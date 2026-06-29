# python3
# -*- coding: utf-8 -*-
"""
FastAPI Web 应用
创建 FastAPI 应用实例，定义所有 Web API 路由
"""

import asyncio
import json
import os
import platform
import re
import secrets
import shutil
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from nonebot import get_bots, get_loaded_plugins, logger

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    psutil = None  # type: ignore
    HAS_PSUTIL = False

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    httpx = None  # type: ignore
    HAS_HTTPX = False

from .auth import _check_auth, _auth_data, _active_tokens, _hash_pw, _save_auth
from .templates import LOGIN_HTML, DASHBOARD_HTML
from .config_editor import (
    _is_external_plugin,
    _parse_plugin_matchers,
    _resolve_plugin_file,
    _parse_plugin_config_full,
    _update_plugin_config,
    _update_config_py,
    _update_matcher_trigger,
    _read_json_file,
    _write_json_file,
)

from .log_bridge import (
    collect_logs as _collect_logs,
    freeze_error_tracking,
    get_cmd_usage_summary,
    get_error_modules,
    get_msg_counts,
    get_top_users,
    record_cmd_usage,
)


# ==================== FastAPI 应用 ====================

def create_app(start_time: float, data_dir: Path) -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="LiuYing Web UI",
        description="NoneBot2 机器人管理面板",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
    )

    # ---- 主页（未登录显示登录页） ----
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        from fastapi.responses import HTMLResponse as _HTMLResponse
        if _check_auth(request):
            return _HTMLResponse(
                content=DASHBOARD_HTML,
                headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
            )
        return _HTMLResponse(content=LOGIN_HTML)

    # ---- 登录 ----
    @app.post("/api/login")
    async def login(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        username = body.get("username", "")
        password = body.get("password", "")
        if username != _auth_data.get("username", "admin"):
            logger.warning(f"Web UI 登录失败: 用户名错误 ({username})")
            return JSONResponse({"error": "用户名或密码错误"}, status_code=401)
        pw_hash = _hash_pw(password)
        stored_hash = _auth_data.get("password_hash", "")
        if pw_hash != stored_hash:
            logger.warning(f"Web UI 登录失败: 密码不匹配 (输入hash={pw_hash[:16]}..., 存储hash={stored_hash[:16]}...)")
            return JSONResponse({"error": "用户名或密码错误"}, status_code=401)
        token = secrets.token_hex(32)
        _active_tokens[token] = time.time() + 86400
        resp = JSONResponse({
            "success": True,
            "token": token,
            "first_login": _auth_data.get("first_login", False),
            "message": "登录成功" + ("，请修改默认密码" if _auth_data.get("first_login") else ""),
        })
        resp.set_cookie("lhc_token", token, max_age=86400, httponly=True)
        return resp

    # ---- 修改密码 ----
    @app.post("/api/change-password")
    async def change_password(request: Request):
        if not _check_auth(request):
            return JSONResponse({"error": "请先登录"}, status_code=401)
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        new_pw = body.get("new_password", "")
        if len(new_pw) < 6:
            return JSONResponse({"error": "密码至少 6 位"}, status_code=400)
        _auth_data["password_hash"] = _hash_pw(new_pw)
        _auth_data["first_login"] = False
        _save_auth(_auth_data)
        return {"success": True, "message": "密码已修改"}

    # ---- 登出 ----
    @app.post("/api/logout")
    async def logout(request: Request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            token = request.cookies.get("lhc_token", "")
        _active_tokens.pop(token, None)
        resp = JSONResponse({"success": True})
        resp.delete_cookie("lhc_token")
        return resp

    # ---- 健康检查（无需认证） ----
    @app.get("/api/ping")
    async def ping():
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

    # ---- 认证中间件（保护所有 /api/ 路径，ping/login/change-password/logout 除外） ----
    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        if request.url.path.startswith("/api/") and request.url.path not in (
            "/api/ping", "/api/login", "/api/change-password", "/api/logout"
        ):
            if not _check_auth(request):
                resp = JSONResponse({"error": "请先登录"}, status_code=401)
                resp.delete_cookie("lhc_token")
                return resp
        return await call_next(request)

    # ---- 系统状态 ----
    # 检测 AI 对话插件是否可用（支持 site-packages 和本地插件两种安装方式）
    _AICHAT_AVAILABLE = False

    # 1) 已由 NoneBot 加载（本地插件目录 src/plugins/）
    if "src.plugins.nonebot_plugin_aichat_baize" in sys.modules:
        _AICHAT_AVAILABLE = True
    # 2) pip 安装的包
    elif "nonebot_plugin_aichat_baize" in sys.modules:
        _AICHAT_AVAILABLE = True
    # 3) 直接 import 尝试
    if not _AICHAT_AVAILABLE:
        for _mod_name in ("nonebot_plugin_aichat_baize", "src.plugins.nonebot_plugin_aichat_baize"):
            try:
                __import__(_mod_name)
                _AICHAT_AVAILABLE = True
                break
            except ImportError:
                pass
    # 4) find_spec 文件系统定位
    if not _AICHAT_AVAILABLE:
        try:
            from importlib.util import find_spec
            _AICHAT_AVAILABLE = (
                find_spec("nonebot_plugin_aichat_baize") is not None
                or find_spec("src.plugins.nonebot_plugin_aichat_baize") is not None
            )
        except Exception:
            pass
    # 5) 本地目录存在性兜底
    if not _AICHAT_AVAILABLE:
        _local_aichat = Path(__file__).parent.parent / "nonebot_plugin_aichat_baize"
        if _local_aichat.is_dir() and (_local_aichat / "__init__.py").is_file():
            _AICHAT_AVAILABLE = True

    @app.get("/api/status")
    async def get_status():
        if HAS_PSUTIL:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.3)
            except Exception:
                cpu_percent = 0.0
            mem = psutil.virtual_memory()
            try:
                disk = psutil.disk_usage(str(Path.cwd().anchor))
            except Exception:
                disk = psutil.disk_usage("/")
        else:
            cpu_percent = 0.0
            mem = type('', (), {'total': 0, 'used': 0, 'percent': 0})()
            disk = type('', (), {'total': 0, 'used': 0, 'percent': 0})()

        bots = get_bots()
        bot_count = len(bots)

        plugins = get_loaded_plugins()
        plugin_count = len(plugins)

        uptime = time.time() - start_time

        return {
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count() if HAS_PSUTIL else 0,
            "memory_total": mem.total,
            "memory_used": mem.used,
            "memory_percent": mem.percent,
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_percent": disk.percent,
            "uptime_seconds": uptime,
            "start_time": datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S"),
            "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "python_version": sys.version,
            "nonebot_version": "2.4.4",
            "bot_count": bot_count,
            "plugin_count": plugin_count,
            "recv_msg_count": get_msg_counts()["recv"],
            "send_msg_count": get_msg_counts()["sent"],
            "aichat_available": _AICHAT_AVAILABLE,
            "help_available": _HELP_AVAILABLE,
        }

    # ---- 插件列表 ----
    @app.get("/api/plugins")
    async def get_plugins():
        loaded_plugins = get_loaded_plugins()
        error_mods = get_error_modules()

        # 构建成功加载的模块名集合
        loaded_names: set = set()
        loaded_meta: dict = {}
        for p in loaded_plugins:
            meta = p.metadata if hasattr(p, 'metadata') else None
            module_name = p.name
            loaded_names.add(module_name)
            # 短名也加入（如 src.plugins.xxx → xxx）
            short = module_name.rsplit(".", 1)[-1] if "." in module_name else module_name
            loaded_names.add(short)
            loaded_meta[module_name] = meta
            loaded_meta[short] = meta

        result: list = []
        seen_modules: set = set()

        # 1) 成功加载的插件
        plugins_dir = Path(__file__).parent.parent
        for p in loaded_plugins:
            meta = p.metadata if hasattr(p, 'metadata') else None
            module_name = p.name
            if module_name in seen_modules:
                continue
            seen_modules.add(module_name)
            short_name = module_name.rsplit(".", 1)[-1] if "." in module_name else module_name
            has_error = module_name in error_mods or short_name in error_mods
            # 检查文件是否已被禁用（本地 .disabled 后缀 或 外部插件不在 TOML 列表中）
            is_disabled = (plugins_dir / f"{short_name}.py.disabled").is_file() \
                       or (plugins_dir / f"{short_name}.disabled").is_dir()
            # 检查是否为 pip 外部插件
            plugin_file = _resolve_plugin_file(module_name)
            is_external = _is_external_plugin(plugin_file) if plugin_file else False
            # 外部插件：如果在 TOML plugins 列表中找不到，也视为禁用
            if is_external and not is_disabled:
                try:
                    toml_text = (Path.cwd() / "pyproject.toml").read_text(encoding="utf-8")
                    tm = re.search(r'plugins\s*=\s*\[([^\]]*)\]', toml_text)
                    if tm:
                        toml_list = [n.strip().strip('"').strip("'") for n in tm.group(1).split(",") if n.strip()]
                        if module_name not in toml_list and short_name not in toml_list:
                            is_disabled = True
                except Exception:
                    pass
            result.append({
                "name": meta.name if meta and meta.name else short_name,
                "description": meta.description if meta and meta.description else "",
                "module": module_name,
                "loaded": not has_error and not is_disabled,
                "disabled": is_disabled,
                "external": is_external,
            })

        # 2) 扫描 src/plugins 目录，找出加载失败的单文件插件和目录插件

        def _extract_meta(file_path: Path) -> tuple:
            """从 .py 文件中提取 __plugin_meta__ 的名称和描述"""
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                import ast as _ast
                tree = _ast.parse(text)
                for node in _ast.walk(tree):
                    if isinstance(node, _ast.Assign):
                        for target in node.targets:
                            if hasattr(target, 'id') and target.id == '__plugin_meta__':
                                dn, desc = "", ""
                                try:
                                    for kw in node.value.keywords:
                                        if kw.arg == 'name':
                                            dn = kw.value.value if hasattr(kw.value, 'value') else ""
                                        elif kw.arg == 'description':
                                            desc = kw.value.value if hasattr(kw.value, 'value') else ""
                                except Exception:
                                    pass
                                return dn, desc
                return "", ""
            except SyntaxError as e:
                return "", f"语法错误: {e.msg} (第 {e.lineno} 行)"
            except Exception as e:
                return "", f"无法解析: {e}"

        # 2a) 单文件插件 (.py)
        for f in sorted(plugins_dir.glob("*.py")):
            if f.name.startswith("_"):
                continue
            module_name = f.stem
            if module_name in loaded_names or module_name in seen_modules:
                continue
            seen_modules.add(module_name)
            dn, desc = _extract_meta(f)
            result.append({
                "name": dn or module_name,
                "description": desc,
                "module": module_name,
                "loaded": False,
            })

        # 2b) 目录插件 (xxx/__init__.py)
        for d in sorted(plugins_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
                continue
            init_file = d / "__init__.py"
            if not init_file.is_file():
                continue
            module_name = d.name
            if module_name in loaded_names or module_name in seen_modules:
                continue
            seen_modules.add(module_name)
            dn, desc = _extract_meta(init_file)
            result.append({
                "name": dn or module_name,
                "description": desc,
                "module": module_name,
                "loaded": False,
            })

        # 3) 错误日志中提及但不在以上任何一个列表的（如 pyproject.toml 中的 pip 插件）
        for err_mod in error_mods:
            if err_mod in seen_modules:
                continue
            if err_mod in ("nonebot", "src", "stdout"):
                continue  # 框架 logger，不是插件
            seen_modules.add(err_mod)
            result.append({
                "name": err_mod,
                "description": "插件加载失败（依赖未安装或导入错误）",
                "module": err_mod,
                "loaded": False,
            })

        # 4) 扫描禁用的插件（.py.disabled / .disabled 目录）
        for f in sorted(plugins_dir.glob("*.py.disabled")):
            module_name = f.stem.replace(".py", "")  # xxx.py.disabled → xxx
            if module_name in seen_modules:
                continue
            seen_modules.add(module_name)
            dn, desc = _extract_meta(f)
            result.append({
                "name": dn or module_name,
                "description": desc or "插件已禁用",
                "module": module_name,
                "loaded": False,
                "disabled": True,
            })

        for d in sorted(plugins_dir.iterdir()):
            if not d.is_dir() or not d.name.endswith(".disabled"):
                continue
            init_file = d / "__init__.py"
            if not init_file.is_file():
                continue
            module_name = d.name.replace(".disabled", "")  # xxx.disabled → xxx
            if module_name in seen_modules:
                continue
            seen_modules.add(module_name)
            dn, desc = _extract_meta(init_file)
            result.append({
                "name": dn or module_name,
                "description": desc or "插件已禁用",
                "module": module_name,
                "loaded": False,
                "disabled": True,
            })

        # 已加载的排前面，各自按名称升序
        result.sort(key=lambda x: (not x["loaded"], x["name"].lower()))
        return result

    # ---- 插件配置读写 ----
    @app.get("/api/plugins/config")
    async def get_plugin_config(module: str = Query(default="", description="插件模块名")):
        """读取插件的可编辑配置变量 + 关联的 JSON 配置文件"""
        if not module:
            return JSONResponse({"error": "缺少 module 参数"}, status_code=400)

        file_path = _resolve_plugin_file(module)
        if file_path is None:
            # 尝试连字符/下划线互换后再查一次
            alt = module.replace("-", "_") if "-" in module else module.replace("_", "-")
            if alt != module:
                file_path = _resolve_plugin_file(alt)
        if file_path is None:
            logger.warning(f"无法定位插件文件: {module}")
            return JSONResponse({"error": f"无法定位插件文件: {module}"}, status_code=404)

        data = _parse_plugin_config_full(file_path)
        return {
            "module": module,
            **data,
            "note": "Python 常量修改后需重启 Bot 生效；JSON 配置即时生效（下次读取时）",
        }

    @app.post("/api/plugins/config")
    async def update_plugin_config(request: Request):
        """更新插件的配置。Body: {module, changes?: {NAME: new_value}, json_changes?: [{name, content}]}"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)

        module = body.get("module", "")
        changes = body.get("changes", {})
        json_changes = body.get("json_changes", [])
        config_py_changes = body.get("config_py_changes", {})

        if not module:
            return JSONResponse({"error": "缺少 module 字段"}, status_code=400)
        if not changes and not json_changes and not config_py_changes:
            return JSONResponse({"error": "缺少 changes / json_changes / config_py_changes 字段"}, status_code=400)

        # 安全检查 + 路径解析
        file_path = _resolve_plugin_file(module)
        if file_path is None:
            return JSONResponse({"error": f"模块文件不存在: {module}.py 或 {module}/__init__.py"}, status_code=404)

        allowed_dir = Path(__file__).parent.parent.resolve()

        messages = []

        # --- 特殊处理：aichat 插件的 API_KEY / MODEL_ID / API_URL 写入 api_config.json ---
        _API_JSON_KEYS = {"API_KEY", "MODEL_ID", "API_URL"}
        _api_json_changes = {}
        _other_changes = {}
        for k, v in changes.items():
            _key = k[7:] if k.startswith("CONFIG.") else k  # CONFIG.API_KEY → API_KEY
            if _key in _API_JSON_KEYS:
                _api_json_changes[_key] = v
            else:
                _other_changes[k] = v
        logger.info(f"[config-save] module={module} api_changes={_api_json_changes} other_changes={_other_changes}")

        if _api_json_changes:
            # 定位 api_config.json（在 aichat 插件 data/ 子目录下）
            _api_json_path = file_path.parent / "data" / "api_config.json"
            logger.info(f"[config-save] 目标 api_config.json 路径: {_api_json_path} (exists={_api_json_path.exists()})")
            try:
                _current = {}
                if _api_json_path.exists():
                    _current = json.loads(_api_json_path.read_text(encoding="utf-8"))
                _current.update(_api_json_changes)
                _api_json_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(_api_json_path, Path(str(_api_json_path) + ".bak")) if _api_json_path.exists() else None
                _api_json_path.write_text(json.dumps(_current, ensure_ascii=False, indent=2), encoding="utf-8")
                logger.info(f"api_config.json 已更新: {_api_json_changes}")
                messages.append("API 配置已写入 api_config.json（即时生效，升级插件不丢失）")
                # 触发 aichat 的 reload_config 运行时生效
                try:
                    for _mn, _mod in list(sys.modules.items()):
                        if hasattr(_mod, "reload_config") and callable(_mod.reload_config):
                            _mod.reload_config()
                            logger.info(f"已触发 {_mn} 的运行时配置重载")
                            break
                except Exception as _e:
                    logger.warning(f"运行时重载配置失败: {_e}")
            except Exception as _e:
                logger.error(f"写入 api_config.json 失败: {_e}")
                messages.append(f"API 配置写入失败: {_e}")

        # --- Python 常量更新（非 API 密钥的普通配置项）---
        if _other_changes:
            if _update_plugin_config(file_path, _other_changes):
                logger.info(f"插件配置已更新: {module} → {_other_changes}")
                try:
                    for _mn, _mod in list(sys.modules.items()):
                        if hasattr(_mod, "reload_config") and callable(_mod.reload_config):
                            _mod.reload_config()
                            logger.info(f"已触发 {_mn} 的运行时配置重载")
                            break
                except Exception as _e:
                    logger.warning(f"运行时重载配置失败: {_e}")
                messages.append("Python 配置已保存并即时生效")
            else:
                messages.append("Python 配置写入失败（无匹配的配置项）")

        # --- JSON 文件更新 ---
        project_root = Path.cwd()
        for jc in json_changes:
            json_name = jc.get("name", "")
            json_content = jc.get("content", "")
            json_rel = jc.get("path", "")
            if not json_rel:
                continue
            # data/api_config.json 已在上面通过 _api_json_changes 处理，跳过避免覆盖
            if "api_config.json" in json_rel:
                continue
            # 路径相对于项目根目录
            json_path = (project_root / json_rel).resolve()
            # 安全检查：必须在项目根目录或插件目录下
            if (str(project_root.resolve()) not in str(json_path.parent)
                    and str(allowed_dir.resolve()) not in str(json_path.parent)):
                messages.append(f"JSON 文件路径不允许: {json_rel}")
                continue
            if not json_path.exists():
                messages.append(f"JSON 文件不存在: {json_rel}")
                continue
            if _write_json_file(json_path, json_content):
                logger.info(f"JSON 配置已更新: {json_rel}")
                messages.append(f"{json_name} 已保存（即时生效）")
            else:
                messages.append(f"{json_name} 保存失败（JSON 格式错误）")

        # --- 指令触发词更新 ---
        matcher_changes = body.get("matcher_changes", [])
        for mc in matcher_changes:
            mc_var = mc.get("variable", "")
            mc_trigger = mc.get("trigger", "")
            if not mc_var or not mc_trigger:
                continue
            if _update_matcher_trigger(file_path, mc_var, mc_trigger):
                logger.info(f"指令触发词已更新: {mc_var} → {mc_trigger}")
                messages.append(f"指令「{mc_var}」→ 「{mc_trigger}」已保存，重启后生效")
            else:
                messages.append(f"指令「{mc_var}」更新失败")

        # --- config.py 更新 ---
        if config_py_changes:
            config_py_path = file_path.parent / "config.py"
            if config_py_path.is_file() and config_py_path != file_path:
                if _update_config_py(config_py_path, config_py_changes):
                    logger.info(f"config.py 已更新: {config_py_path} → {config_py_changes}")
                    messages.append("config.py 配置已保存，重启后生效")
                else:
                    messages.append("config.py 写入失败")

        if any("已保存" in m or "即时生效" in m for m in messages):
            return {"success": True, "message": "; ".join(messages)}
        else:
            return JSONResponse({"error": "; ".join(messages) or "无变更"}, status_code=500)

    # ---- 插件启用/禁用 ----
    @app.post("/api/plugins/toggle")
    async def toggle_plugin(request: Request):
        """启用或禁用插件（通过重命名文件 + 清理 pycache）"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)

        module = body.get("module", "")
        enabled = body.get("enabled", True)

        # 规范化模块名
        if "." in module:
            module = module.rsplit(".", 1)[-1]

        if not module:
            return JSONResponse({"error": "缺少 module 字段"}, status_code=400)

        # 外部 pip 插件：通过编辑 pyproject.toml 的 plugins 列表实现启停
        plugin_file = _resolve_plugin_file(module)
        if plugin_file and _is_external_plugin(plugin_file):
            toml_path = Path.cwd() / "pyproject.toml"
            if not toml_path.exists():
                return JSONResponse({"error": "pyproject.toml 不存在"}, status_code=500)
            toml_text = toml_path.read_text(encoding="utf-8")
            m = re.search(r'(plugins\s*=\s*\[)([^\]]*)(\])', toml_text)
            if not m:
                return JSONResponse({"error": "未找到 pyproject.toml 中的 plugins 列表"}, status_code=500)
            existing = m.group(2)
            current = [n.strip().strip('"').strip("'") for n in existing.split(",") if n.strip()]
            underscore = module.replace("-", "_")
            hyphen = module.replace("_", "-")
            found = None
            for variant in (module, underscore, hyphen):
                if variant in current:
                    found = variant
                    break
            if enabled and found is None:
                # 启用：添加回列表
                current.append(underscore)
            elif not enabled and found is not None:
                # 禁用：从列表移除
                current.remove(found)
            else:
                status = "已启用" if enabled else "已禁用"
                return {"success": True, "enabled": enabled, "message": f"「{module}」已处于{status}状态"}
            new_plugins = ", ".join(f'"{n}"' for n in current)
            new_text = toml_text[:m.start()] + f'plugins = [{new_plugins}]' + toml_text[m.end():]
            shutil.copy2(toml_path, toml_path.with_suffix(".toml.bak"))
            toml_path.write_text(new_text, encoding="utf-8")
            action = "启用" if enabled else "禁用"
            return {"success": True, "enabled": enabled, "message": f"「{module}」已{action}，重启 Bot 后生效"}
        plugins_dir = Path(__file__).parent.parent

        def _clear_pycache(mod_name: str):
            """删除 __pycache__ 中对应模块的 .pyc 缓存"""
            pycache = plugins_dir / "__pycache__"
            if not pycache.is_dir():
                return
            for pyc in pycache.glob(f"{mod_name}.cpython-*.pyc"):
                try:
                    pyc.unlink()
                except OSError:
                    pass
            # 也检查目录内的 __pycache__
            for d in plugins_dir.iterdir():
                if d.is_dir() and d.name not in ("__pycache__",):
                    inner_cache = d / "__pycache__"
                    if inner_cache.is_dir():
                        for pyc in inner_cache.glob("__init__.cpython-*.pyc"):
                            try:
                                pyc.unlink()
                            except OSError:
                                pass

        # 单文件插件: xxx.py ↔ xxx.py.disabled
        py_file = plugins_dir / f"{module}.py"
        disabled_file = plugins_dir / f"{module}.py.disabled"

        if py_file.is_file():
            if not enabled:
                try:
                    py_file.rename(disabled_file)
                    _clear_pycache(module)
                    logger.info(f"插件已禁用: {module}.py → {module}.py.disabled")
                    return {"success": True, "enabled": False, "message": f"「{module}」已禁用，重启 Bot 后生效"}
                except OSError as e:
                    logger.error(f"禁用插件失败: {module} - {e}")
                    return JSONResponse({"error": f"重命名失败: {e}"}, status_code=500)
            else:
                return {"success": True, "enabled": True, "message": f"「{module}」已处于启用状态"}

        if disabled_file.is_file():
            if enabled:
                try:
                    disabled_file.rename(py_file)
                    logger.info(f"插件已启用: {module}.py.disabled → {module}.py")
                    return {"success": True, "enabled": True, "message": f"「{module}」已启用，重启 Bot 后生效"}
                except OSError as e:
                    logger.error(f"启用插件失败: {module} - {e}")
                    return JSONResponse({"error": f"重命名失败: {e}"}, status_code=500)
            else:
                return {"success": True, "enabled": False, "message": f"「{module}」已处于禁用状态"}

        # 目录插件: xxx/ ↔ xxx.disabled/
        pkg_dir = plugins_dir / module
        disabled_dir = plugins_dir / f"{module}.disabled"

        if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
            if not enabled:
                try:
                    pkg_dir.rename(disabled_dir)
                    _clear_pycache(module)
                    logger.info(f"目录插件已禁用: {module}/ → {module}.disabled/")
                    return {"success": True, "enabled": False, "message": f"「{module}」已禁用，重启 Bot 后生效"}
                except OSError as e:
                    logger.error(f"禁用目录插件失败: {module} - {e}")
                    return JSONResponse({"error": f"重命名失败: {e}"}, status_code=500)
            else:
                return {"success": True, "enabled": True, "message": f"「{module}」已处于启用状态"}

        if disabled_dir.is_dir() and (disabled_dir / "__init__.py").is_file():
            if enabled:
                try:
                    disabled_dir.rename(pkg_dir)
                    logger.info(f"目录插件已启用: {module}.disabled/ → {module}/")
                    return {"success": True, "enabled": True, "message": f"「{module}」已启用，重启 Bot 后生效"}
                except OSError as e:
                    logger.error(f"启用目录插件失败: {module} - {e}")
                    return JSONResponse({"error": f"重命名失败: {e}"}, status_code=500)
            else:
                return {"success": True, "enabled": False, "message": f"「{module}」已处于禁用状态"}

        return JSONResponse({"error": f"未找到插件: {module}（请确认模块名正确，不含 src.plugins. 前缀）"}, status_code=404)

    # ---- Bot 列表 ----
    @app.get("/api/bots")
    async def get_bot_list():
        bots = get_bots()
        result = []
        for bot_id, bot in bots.items():
            info = {
                "self_id": str(bot_id),
                "adapter": "",
                "nickname": "",
            }
            try:
                if hasattr(bot, 'adapter'):
                    info["adapter"] = bot.adapter.get_name() if hasattr(bot.adapter, 'get_name') else type(bot.adapter).__name__
            except Exception:
                info["adapter"] = "OneBot V11"
            try:
                if hasattr(bot, '_self_info') and bot._self_info:
                    info["nickname"] = bot._self_info.get("nickname", "")
            except Exception:
                pass
            result.append(info)
        return result

    # ---- 日志 ----
    @app.get("/api/logs")
    async def get_logs(limit: int = Query(default=200, ge=10, le=1000)):
        logs = _collect_logs(limit)
        return logs

    # ---- 指令使用统计 ----
    @app.get("/api/cmd-stats")
    async def get_cmd_stats():
        """返回指令使用统计（on_command / on_fullmatch / on_message）"""
        return get_cmd_usage_summary()

    # ---- 管理员管理 ----
    @app.get("/api/admins")
    async def get_admins():
        return {"admins": _auth_data.get("admins", [])}

    @app.post("/api/admins/add")
    async def add_admin(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        qq = str(body.get("qq", "")).strip()
        if not qq.isdigit():
            return JSONResponse({"error": "QQ 号需为纯数字"}, status_code=400)
        admins = _auth_data.setdefault("admins", [])
        if qq in admins:
            return {"success": True, "message": f"管理员 {qq} 已存在"}
        admins.append(qq)
        _save_auth(_auth_data)
        return {"success": True, "message": f"已添加管理员 {qq}"}

    @app.post("/api/admins/remove")
    async def remove_admin(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        qq = str(body.get("qq", "")).strip()
        admins = _auth_data.get("admins", [])
        if qq not in admins:
            return {"success": True, "message": f"管理员 {qq} 不存在"}
        admins.remove(qq)
        _save_auth(_auth_data)
        return {"success": True, "message": f"已移除管理员 {qq}"}

    # ---- Bot 用户信息 ----
    @app.get("/api/bot-info")
    async def get_bot_info():
        """获取 Bot 账号信息（QQ号、头像、好友/群数量）"""
        bots = get_bots()
        if not bots:
            return JSONResponse({"error": "没有已连接的 Bot"}, status_code=503)
        bot = list(bots.values())[0]
        try:
            info = await bot.get_login_info()
            qq = str(info.get("user_id", ""))
            nickname = info.get("nickname", "")
            avatar = f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"
        except Exception:
            qq, nickname, avatar = str(bot.self_id), "", ""

        friends, groups = 0, 0
        try:
            fl = await bot.get_friend_list()
            friends = len(fl) if isinstance(fl, list) else 0
        except Exception:
            pass
        try:
            gl = await bot.get_group_list()
            groups = len(gl) if isinstance(gl, list) else 0
        except Exception:
            pass

        return {
            "qq": qq,
            "nickname": nickname,
            "avatar": avatar,
            "friends": friends,
            "groups": groups,
            "msg_recv": get_msg_counts()["recv"],
            "msg_sent": get_msg_counts()["sent"],
        }

    # ---- Bot 好友/群聊详情 ----
    @app.get("/api/bot-info/friends")
    async def get_friend_list():
        bots = get_bots()
        if not bots:
            return JSONResponse({"error": "没有已连接的 Bot"}, status_code=503)
        bot = list(bots.values())[0]
        try:
            fl = await bot.get_friend_list()
            friends = []
            for f in (fl if isinstance(fl, list) else []):
                qq = str(f.get("user_id", ""))
                friends.append({
                    "qq": qq,
                    "nickname": f.get("nickname", ""),
                    "remark": f.get("remark", ""),
                    "avatar": f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=100",
                })
            return {"friends": friends, "total": len(friends)}
        except Exception:
            return JSONResponse({"error": "获取好友列表失败"}, status_code=500)

    @app.get("/api/bot-info/top-users")
    async def get_top_private_users():
        return {"users": get_top_users(10)}

    @app.get("/api/bot-info/groups")
    async def get_group_list():
        bots = get_bots()
        if not bots:
            return JSONResponse({"error": "没有已连接的 Bot"}, status_code=503)
        bot = list(bots.values())[0]
        try:
            gl = await bot.get_group_list()
            groups = []
            for g in (gl if isinstance(gl, list) else []):
                qq = str(g.get("group_id", ""))
                groups.append({
                    "id": qq,
                    "name": g.get("group_name", ""),
                    "avatar": f"https://p.qlogo.cn/gh/{qq}/{qq}/100/",
                    "member_count": g.get("member_count", 0),
                    "max_member_count": g.get("max_member_count", 0),
                })
            return {"groups": groups, "total": len(groups)}
        except Exception:
            return JSONResponse({"error": "获取群列表失败"}, status_code=500)

    # ---- 删除好友 / 退出群聊 ----
    @app.post("/api/bot-info/friends/delete")
    async def delete_friend(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        qq = body.get("qq", "")
        if not qq:
            return JSONResponse({"error": "缺少 qq 参数"}, status_code=400)
        bots = get_bots()
        if not bots:
            return JSONResponse({"error": "没有已连接的 Bot"}, status_code=503)
        bot = list(bots.values())[0]
        try:
            await bot.call_api("delete_friend", user_id=int(qq))
            return {"success": True, "message": f"已删除好友 {qq}"}
        except Exception as e:
            return JSONResponse({"error": f"删除失败: {e}"}, status_code=500)

    @app.post("/api/bot-info/groups/leave")
    async def leave_group(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        group_id = body.get("group_id", "")
        if not group_id:
            return JSONResponse({"error": "缺少 group_id 参数"}, status_code=400)
        bots = get_bots()
        if not bots:
            return JSONResponse({"error": "没有已连接的 Bot"}, status_code=503)
        bot = list(bots.values())[0]
        try:
            await bot.call_api("set_group_leave", group_id=int(group_id))
            return {"success": True, "message": f"已退出群聊 {group_id}"}
        except Exception as e:
            return JSONResponse({"error": f"退群失败: {e}"}, status_code=500)

    # ---- 一键启用/禁用 ----
    @app.post("/api/plugins/toggle-all")
    async def toggle_all_plugins(request: Request):
        """一键启用或禁用所有插件（本地 + 外部 pip）"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        enabled = body.get("enabled", True)
        plugins_dir = Path(__file__).parent.parent
        toggled = 0
        action = "启用" if enabled else "禁用"

        # ── 本地插件：文件重命名 ──
        if enabled:
            for f in sorted(plugins_dir.glob("*.py.disabled")):
                module = f.stem.replace(".py", "")
                target = plugins_dir / f"{module}.py"
                try: f.rename(target); toggled += 1
                except OSError: pass
            for d in sorted(plugins_dir.iterdir()):
                if not d.is_dir() or not d.name.endswith(".disabled"): continue
                if not (d / "__init__.py").is_file(): continue
                target = plugins_dir / d.name.replace(".disabled", "")
                try: d.rename(target); toggled += 1
                except OSError: pass
        else:
            for f in sorted(plugins_dir.glob("*.py")):
                if f.name.startswith("_") or f.name == "web_ui.py": continue
                target = plugins_dir / f"{f.name}.disabled"
                try: f.rename(target); toggled += 1
                except OSError: pass
            for d in sorted(plugins_dir.iterdir()):
                if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."): continue
                if not (d / "__init__.py").is_file(): continue
                target = plugins_dir / f"{d.name}.disabled"
                try: d.rename(target); toggled += 1
                except OSError: pass

        # ── 外部 pip 插件：编辑 pyproject.toml ──
        toml_path = Path.cwd() / "pyproject.toml"
        if toml_path.exists():
            toml_text = toml_path.read_text(encoding="utf-8")
            tm = re.search(r'(plugins\s*=\s*\[)([^\]]*)(\])', toml_text)
            if tm:
                current = [n.strip().strip('"').strip("'") for n in tm.group(2).split(",") if n.strip()]
                # 收集所有已安装的外部插件模块名
                ext_modules = set()
                for p in get_loaded_plugins():
                    pf = _resolve_plugin_file(p.name)
                    if pf and _is_external_plugin(pf):
                        mod = p.name.rsplit(".", 1)[-1] if "." in p.name else p.name
                        ext_modules.add(mod.replace("-", "_"))
                if enabled:
                    # 添加所有外部插件到列表
                    added = [m for m in ext_modules if m not in current]
                    current.extend(added)
                    toggled += len(added)
                else:
                    # 移除所有外部插件
                    removed = [m for m in current if m in ext_modules]
                    for m in removed:
                        current.remove(m)
                    toggled += len(removed)

                new_plugins = ", ".join(f'"{n}"' for n in current)
                new_text = toml_text[:tm.start()] + f'plugins = [{new_plugins}]' + toml_text[tm.end():]
                shutil.copy2(toml_path, toml_path.with_suffix(".toml.bak"))
                toml_path.write_text(new_text, encoding="utf-8")

        note = "，请重启 Bot 使其生效" if toggled > 0 else ""
        return {"success": True, "message": f"已{action} {toggled} 个插件{note}"}

    # ---- 全部指令列表 ----
    @app.get("/api/commands")
    async def get_all_commands():
        """扫描所有插件（本地 + pip 外部），按类型分类返回全部指令触发词"""
        plugins_dir = Path(__file__).parent.parent
        result = {"on_command": [], "on_fullmatch": [], "on_alconna": [], "on_startswith": [], "on_regex": [], "on_endswith": [], "on_message": []}
        seen_modules = set()

        def _scan_dir(plugin_dir: Path, module_name: str):
            """扫描目录插件：__init__.py + 其他 .py 文件 + 子目录"""
            if module_name in seen_modules:
                return
            seen_modules.add(module_name)
            init = plugin_dir / "__init__.py"
            files_to_scan = [init] if init.is_file() else []
            # 同目录其他 .py（如 commands.py、matchers.py）
            for sibling in sorted(plugin_dir.glob("*.py")):
                if sibling.name != "__init__.py" and not sibling.name.startswith("_"):
                    files_to_scan.append(sibling)
            # 子目录
            for sub in sorted(plugin_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith("_") or sub.name.startswith("."):
                    continue
                for py in sorted(sub.glob("*.py")):
                    if not py.name.startswith("_"):
                        files_to_scan.append(py)
            for fp in files_to_scan:
                try:
                    for m in _parse_plugin_matchers(fp):
                        result.setdefault(m["type"], []).append({
                            "trigger": m["trigger"],
                            "variable": m["variable"],
                            "module": module_name,
                        })
                except Exception:
                    pass

        # 本地单文件插件
        for f in sorted(plugins_dir.glob("*.py")):
            if not f.name.startswith("_") and f.name != "web_ui.py":
                if f.stem not in seen_modules:
                    seen_modules.add(f.stem)
                    try:
                        for m in _parse_plugin_matchers(f):
                            result.setdefault(m["type"], []).append({
                                "trigger": m["trigger"], "variable": m["variable"], "module": f.stem,
                            })
                    except Exception:
                        pass
        # 本地目录插件
        for d in sorted(plugins_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
                continue
            if (d / "__init__.py").is_file():
                _scan_dir(d, d.name)

        # pip 外部插件
        for p in get_loaded_plugins():
            module_name = p.name
            short = module_name.rsplit(".", 1)[-1] if "." in module_name else module_name
            if short in seen_modules or module_name in seen_modules:
                continue
            plugin_file = _resolve_plugin_file(module_name)
            if plugin_file and _is_external_plugin(plugin_file):
                _scan_dir(plugin_file.parent, module_name)

        # 排序
        for key in result:
            result[key].sort(key=lambda x: (x["module"], x["trigger"]))

        return {
            "on_command": result["on_command"],
            "on_fullmatch": result["on_fullmatch"],
            "on_alconna": result["on_alconna"],
            "on_startswith": result["on_startswith"],
            "on_regex": result["on_regex"],
            "on_endswith": result["on_endswith"],
            "on_message": result["on_message"],
        }

    # ---- 收藏 API: 导出状态 ----
    @app.get("/api/export/status")
    async def export_status():
        """JSON 格式导出当前状态"""
        status = await get_status()
        plugins = await get_plugins()
        bots = await get_bot_list()
        return {
            "export_time": datetime.now().isoformat(),
            "status": status,
            "plugins": plugins,
            "bots": bots,
        }

    # ---- 插件商店 ----
    def _trigger_reload():
        """touch bot.py 触发 nb run --reload 热重载"""
        bot_py = Path.cwd() / "bot.py"
        if bot_py.exists():
            text = bot_py.read_text(encoding="utf-8")
            bot_py.write_text(text, encoding="utf-8")
            return True
        return False

    _store_cache = {"data": None, "time": 0}

    @app.get("/api/store")
    async def get_store_plugins(search: str = Query(default=""), tag: str = Query(default="")):
        import time as _time
        if not HAS_HTTPX:
            return JSONResponse({"error": "httpx 未安装，请执行: pip install httpx"}, status_code=500)

        cache_ttl = 600
        now = _time.time()
        if _store_cache["data"] is None or now - _store_cache["time"] > cache_ttl:
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    resp = await client.get("https://registry.nonebot.dev/plugins.json")
                    if resp.status_code == 200:
                        _store_cache["data"] = resp.json()
                        _store_cache["time"] = now
            except Exception:
                if _store_cache["data"] is None:
                    return JSONResponse({"error": "无法连接插件商店"}, status_code=502)

        plugins = _store_cache["data"] or []
        if search:
            q = search.lower()
            plugins = [p for p in plugins if q in (p.get("name", "") + p.get("desc", "") + p.get("module_name", "") + p.get("author", "")).lower()]
        if tag:
            plugins = [p for p in plugins if any(t["label"] == tag for t in p.get("tags", []))]

        installed = {p.name for p in get_loaded_plugins()}
        for p in plugins:
            p["installed"] = p.get("module_name", "") in installed

        return {"total": len(plugins), "plugins": plugins[:200]}

    @app.post("/api/store/install")
    async def install_plugin(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)
        project = (body.get("project", "") or body.get("module_name", "")).strip()
        module_name = body.get("module_name", project).strip()
        if not project or not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', project):
            return JSONResponse({"error": "无效的包名"}, status_code=400)

        def _run_pip():
            import subprocess
            r = subprocess.run(
                [sys.executable, "-m", "pip", "install", project],
                capture_output=True, text=True, timeout=120,
            )
            return r.returncode, r.stderr

        try:
            code, err = await asyncio.to_thread(_run_pip)
            if code == 0:
                logger.info(f"插件已安装: {project}")

                # pip 包名（连字符）转 Python 模块名（下划线）
                toml_module = module_name.replace("-", "_")

                # 自动添加 pyproject.toml 的 plugins 列表
                toml_path = Path.cwd() / "pyproject.toml"
                try:
                    if toml_path.exists():
                        toml_text = toml_path.read_text(encoding="utf-8")
                        # 匹配 plugins = [...] 行
                        plugins_match = re.search(
                            r'(plugins\s*=\s*\[)([^\]]*)(\])', toml_text
                        )
                        if plugins_match:
                            existing = plugins_match.group(2)
                            current_list = [
                                n.strip().strip('"').strip("'")
                                for n in existing.split(",") if n.strip()
                            ]
                            if toml_module not in current_list:
                                # 同时清理旧的连字符版本
                                hyphen_ver = module_name.replace("_", "-")
                                for bad in [hyphen_ver, module_name]:
                                    if bad != toml_module and bad in current_list:
                                        current_list.remove(bad)
                                current_list.append(toml_module)
                                new_plugins = ", ".join(f'"{n}"' for n in current_list)
                                new_text = (
                                    toml_text[:plugins_match.start()]
                                    + f'plugins = [{new_plugins}]'
                                    + toml_text[plugins_match.end():]
                                )
                                # 备份
                                shutil.copy2(toml_path, toml_path.with_suffix(".toml.bak"))
                                toml_path.write_text(new_text, encoding="utf-8")
                                logger.info(f"pyproject.toml 已更新: 添加 {toml_module}")
                                _store_cache["data"] = None
                                _trigger_reload()
                                return {
                                    "success": True,
                                    "message": f"「{toml_module}」安装成功，已自动添加到 pyproject.toml，正在热重载..."
                                }
                except Exception as e:
                    logger.warning(f"自动更新 pyproject.toml 失败: {e}")

                _store_cache["data"] = None
                return {"success": True, "message": f"「{toml_module}」安装成功，请在 pyproject.toml 中添加后重启 Bot"}
            else:
                return JSONResponse({"error": f"安装失败: {err[-500:]}"}, status_code=500)
        except Exception as e:
            logger.error(f"插件安装异常: {project} - {e}")
            return JSONResponse({"error": f"执行失败: {e}"}, status_code=500)

    # ---- GitHub 插件下载 ----
    _github_plugins_cache = {"data": None, "time": 0}

    @app.get("/api/github-plugins")
    async def get_github_plugins(search: str = Query(default="")):
        """获取 GitHub 用户 sangonomiya249 的插件仓库列表"""
        import time as _time
        if not HAS_HTTPX:
            return JSONResponse({"error": "httpx 未安装，请执行: pip install httpx"}, status_code=500)

        cache_ttl = 300  # 5分钟缓存
        now = _time.time()
        if _github_plugins_cache["data"] is None or now - _github_plugins_cache["time"] > cache_ttl:
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    resp = await client.get(
                        "https://api.github.com/users/sangonomiya249/repos",
                        params={"per_page": 100, "sort": "updated"},
                        headers={"Accept": "application/vnd.github+json", "User-Agent": "Baize-WebUI"},
                    )
                    if resp.status_code == 200:
                        repos = resp.json()
                        # 展示所有仓库，标记是否为 NoneBot 插件
                        nonebot_repos = []
                        for repo in repos:
                            if repo.get("fork", False) or repo.get("archived", False):
                                continue  # 跳过 fork 和已归档的仓库
                            name = repo.get("name", "")
                            desc = repo.get("description") or ""
                            topics = repo.get("topics", [])
                            show_repo = {
                                "name": name,
                                "description": desc,
                                "html_url": repo.get("html_url", ""),
                                "stars": repo.get("stargazers_count", 0),
                                "updated_at": repo.get("updated_at", ""),
                                "language": repo.get("language", ""),
                                "topics": topics,
                                "default_branch": repo.get("default_branch", "main"),
                                "clone_url": repo.get("clone_url", ""),
                            }
                            nonebot_repos.append(show_repo)
                        _github_plugins_cache["data"] = nonebot_repos
                        _github_plugins_cache["time"] = now
                        logger.info(f"GitHub 插件仓库缓存已更新: {len(nonebot_repos)} 个")
            except Exception as e:
                logger.warning(f"获取 GitHub 仓库列表失败: {e}")
                if _github_plugins_cache["data"] is None:
                    return JSONResponse({"error": f"无法连接 GitHub API: {e}"}, status_code=502)

        plugins = _github_plugins_cache["data"] or []
        if search:
            q = search.lower()
            plugins = [p for p in plugins if q in (p["name"] + p["description"]).lower()]

        # 标记已安装状态（检查已加载插件 + 本地 plugins 目录）
        loaded_names = {p.name for p in get_loaded_plugins()}
        plugins_dir = Path(__file__).parent.parent
        local_names = set()
        try:
            for item in plugins_dir.iterdir():
                if item.is_dir() and not item.name.startswith('_') and not item.name.startswith('.'):
                    local_names.add(item.name)
                    local_names.add(item.name.replace("_", "-"))
                elif item.is_file() and item.suffix == '.py' and not item.name.startswith('_'):
                    local_names.add(item.stem)
                    local_names.add(item.stem.replace("_", "-"))
        except Exception:
            pass
        for p in plugins:
            name = p["name"]
            p["installed"] = name in loaded_names or name in local_names or name.replace("-", "_") in loaded_names

        return {"total": len(plugins), "plugins": plugins[:200]}

    @app.post("/api/github-plugins/install")
    async def install_github_plugin(request: Request):
        """从 GitHub 下载/更新插件到 plugins 目录（通过 API 下载 zip，避免 git 被墙）"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)

        repo_name = body.get("repo_name", "").strip()
        branch = body.get("branch", "").strip() or "main"

        if not repo_name or not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', repo_name):
            return JSONResponse({"error": "无效的仓库名"}, status_code=400)
        if not re.match(r'^[a-zA-Z0-9._/-]+$', branch):
            return JSONResponse({"error": "无效的分支名"}, status_code=400)

        if not HAS_HTTPX:
            return JSONResponse({"error": "httpx 未安装，请执行: pip install httpx"}, status_code=500)

        plugins_dir = Path(__file__).parent.parent  # bot 的 plugins 目录
        target_path = plugins_dir / repo_name
        action = "更新"

        async def _download_and_extract():
            nonlocal action
            import io
            import zipfile
            import tempfile

            # 更新时保留用户数据的目录（不覆盖其内容）
            _PRESERVE_DIRS = {'data', '__pycache__', '.git'}
            # 更新时保留用户数据的文件（不覆盖）
            _PRESERVE_FILES = {'config.json', 'auth.json', '.env', '.env.local'}
            # 更新时允许复制的资源文件扩展名
            _RESOURCE_EXTS = {
                '.py', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico',
                '.html', '.css', '.js', '.json', '.txt', '.md',
                '.ttf', '.woff', '.woff2', '.otf',
                '.yaml', '.yml', '.toml', '.ini', '.cfg',
            }

            def _copy_py_only(src: Path, dst: Path):
                """更新复制：覆盖 .py 和资源文件，保留 data/ 等用户数据目录"""
                if not dst.exists():
                    dst.mkdir(parents=True, exist_ok=True)
                for item in src.iterdir():
                    dst_item = dst / item.name
                    if item.is_dir():
                        if item.name in _PRESERVE_DIRS:
                            continue  # 跳过用户数据目录，不进入
                        _copy_py_only(item, dst_item)
                    elif item.suffix.lower() in _RESOURCE_EXTS:
                        if item.name in _PRESERVE_FILES:
                            continue  # 跳过用户配置文件
                        shutil.copy2(str(item), str(dst_item))

            # 1. 下载 zip
            zip_url = f"https://api.github.com/repos/sangonomiya249/{repo_name}/zipball/{branch}"
            async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
                resp = await client.get(
                    zip_url,
                    headers={"Accept": "application/vnd.github+json", "User-Agent": "Baize-WebUI"},
                )
                if resp.status_code != 200:
                    error_msg = f"GitHub API 返回 {resp.status_code}"
                    try:
                        error_detail = resp.json().get("message", "")
                        if error_detail:
                            error_msg += f": {error_detail}"
                    except Exception:
                        pass
                    return False, error_msg

                zip_data = resp.content

            # 2. 用临时文件写入 zip（避免内存问题）
            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
                tmp.write(zip_data)
                tmp_path = tmp.name

            try:
                # 3. 解压到临时目录
                extract_dir = tempfile.mkdtemp()
                with zipfile.ZipFile(tmp_path, 'r') as zf:
                    zf.extractall(extract_dir)

                # 4. GitHub zipball 嵌套结构，在解压树中找到包含 __init__.py 的真正插件根目录
                extracted_items = list(Path(extract_dir).iterdir())
                start_dir = extracted_items[0] if (len(extracted_items) == 1 and extracted_items[0].is_dir()) else Path(extract_dir)

                # 在整个解压树中搜索 __init__.py，以其所在目录为插件根
                source_dir = start_dir
                best_depth = 999
                for py_file in start_dir.rglob("__init__.py"):
                    parent = py_file.parent
                    depth = len(parent.relative_to(start_dir).parts)
                    if depth < best_depth:
                        best_depth = depth
                        source_dir = parent
                logger.info(f"插件根目录: {source_dir} (深度={best_depth})")

                # 5. 安装/更新
                if target_path.exists():
                    # 更新：只覆盖 .py 文件，保留 JSON/数据文件夹等用户配置
                    action = "更新"
                    _copy_py_only(source_dir, target_path)
                else:
                    # 安装：全量复制
                    action = "安装"
                    target_path.mkdir(parents=True, exist_ok=True)
                    for item in source_dir.iterdir():
                        dst = target_path / item.name
                        if item.is_dir():
                            shutil.copytree(str(item), str(dst))
                        else:
                            shutil.copy2(str(item), str(dst))

                # 6. 清理无用的仓库文件（仅删除源里带过来的，不动用户自己的）
                for junk in ['.gitignore', '.gitattributes', '.editorconfig', 'LICENSE', 'README.md', 'CHANGELOG.md']:
                    jp = target_path / junk
                    try:
                        if jp.is_file():
                            jp.unlink()
                    except Exception:
                        pass
                for junk_dir in ['.github', 'tests', 'test', '__pycache__']:
                    jd = target_path / junk_dir
                    try:
                        if jd.is_dir():
                            shutil.rmtree(jd, ignore_errors=True)
                    except Exception:
                        pass

                return True, ""
            finally:
                # 清理临时文件
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
                try:
                    shutil.rmtree(extract_dir, ignore_errors=True)
                except Exception:
                    pass

        try:
            ok, err_msg = await _download_and_extract()
            if ok:
                logger.info(f"GitHub 插件已{action}: {repo_name} -> {target_path}")

                # 清理可能存在的 pip --target 残留 .dist-info 目录
                for leftover in plugins_dir.glob("*.dist-info"):
                    try:
                        shutil.rmtree(leftover, ignore_errors=True)
                        logger.info(f"已清理残留目录: {leftover}")
                    except Exception:
                        pass

                # GitHub 下载的插件安装到 src/plugins/ 目录，
                # 由 plugin_dirs 自动加载，不需要写入 pyproject.toml。
                # 只有 pip 安装的插件（插件商店）才需要写入 toml。

                _github_plugins_cache["data"] = None
                _trigger_reload()
                return {
                    "success": True,
                    "message": f"「{repo_name}」{action}成功 -> plugins/{repo_name}/，正在热重载..."
                }
            else:
                return JSONResponse({"error": f"下载失败: {err_msg}"}, status_code=500)
        except Exception as e:
            logger.error(f"GitHub 插件操作异常: {repo_name} - {e}")
            return JSONResponse({"error": f"执行失败: {e}"}, status_code=500)

    @app.post("/api/plugins/uninstall")
    async def uninstall_plugin(request: Request):
        """卸载插件（本地删除文件 / pip uninstall）"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)

        module = body.get("module", "").strip()
        if "." in module:
            module = module.rsplit(".", 1)[-1]
        if not module:
            return JSONResponse({"error": "缺少 module 字段"}, status_code=400)

        plugins_dir = Path(__file__).parent.parent

        def _rm_pycache(name: str):
            pycache = plugins_dir / "__pycache__"
            if pycache.is_dir():
                for pyc in list(pycache.glob(f"{name}.cpython-*.pyc")):
                    try: pyc.unlink()
                    except OSError: pass

        # ── 本地插件：删除文件/目录 ──
        py_file = plugins_dir / f"{module}.py"
        disabled_file = plugins_dir / f"{module}.py.disabled"
        pkg_dir = plugins_dir / module
        disabled_dir = plugins_dir / f"{module}.disabled"

        targets = []
        if py_file.is_file():
            targets.append(py_file)
        if disabled_file.is_file():
            targets.append(disabled_file)
        if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
            targets.append(pkg_dir)
        if disabled_dir.is_dir() and (disabled_dir / "__init__.py").is_file():
            targets.append(disabled_dir)

        if targets:
            try:
                for t in targets:
                    if t.is_dir():
                        shutil.rmtree(t)
                        _rm_pycache(t.name)
                    else:
                        _rm_pycache(t.stem)
                        t.unlink()
                logger.info(f"本地插件已卸载: {module}")
                _trigger_reload()
                return {"success": True, "message": f"「{module}」已卸载，正在热重载..."}
            except OSError as e:
                logger.error(f"卸载本地插件失败: {module} - {e}")
                return JSONResponse({"error": f"删除失败: {e}"}, status_code=500)

        # ── pip 插件：pip uninstall + 从 pyproject.toml 移除 ──
        plugin_file = _resolve_plugin_file(module)
        if plugin_file and _is_external_plugin(plugin_file):
            def _run_pip_uninstall():
                import subprocess
                r = subprocess.run(
                    [sys.executable, "-m", "pip", "uninstall", "-y", module],
                    capture_output=True, text=True, timeout=60,
                )
                return r.returncode, r.stderr

            try:
                pip_code, pip_err = await asyncio.to_thread(_run_pip_uninstall)
                if pip_code != 0:
                    return JSONResponse({"error": f"pip uninstall 失败: {pip_err[-300:]}"}, status_code=500)
            except Exception as e:
                return JSONResponse({"error": f"pip uninstall 失败: {e}"}, status_code=500)

            # 从 pyproject.toml 移除
            toml_path = Path.cwd() / "pyproject.toml"
            try:
                if toml_path.exists():
                    toml_text = toml_path.read_text(encoding="utf-8")
                    m = re.search(r'(plugins\s*=\s*\[)([^\]]*)(\])', toml_text)
                    if m:
                        existing = m.group(2)
                        current = [n.strip().strip('"').strip("'") for n in existing.split(",") if n.strip()]
                        # 同时匹配下划线和连字符版本
                        underscore = module.replace("-", "_")
                        hyphen = module.replace("_", "-")
                        for variant in (module, underscore, hyphen):
                            if variant in current:
                                current.remove(variant)
                            new_plugins = ", ".join(f'"{n}"' for n in current)
                            new_text = toml_text[:m.start()] + f'plugins = [{new_plugins}]' + toml_text[m.end():]
                            shutil.copy2(toml_path, toml_path.with_suffix(".toml.bak"))
                            toml_path.write_text(new_text, encoding="utf-8")
            except Exception:
                pass

            logger.info(f"pip 插件已卸载: {module}")
            _trigger_reload()
            return {"success": True, "message": f"「{module}」已卸载并从 pyproject.toml 移除，正在热重载..."}

        return JSONResponse({"error": f"未找到插件: {module}"}, status_code=404)

    @app.post("/api/restart")
    async def restart_bot():
        """重启机器人（touch bot.py 触发 nb run 热重载）"""
        logger.info("收到 Web UI 重启指令，触发热重载...")
        try:
            from .log_bridge import _save_cmd_stats
            _save_cmd_stats()
        except Exception:
            pass
        if _trigger_reload():
            return {"success": True, "message": "已触发热重载，Bot 正在重启..."}
        else:
            return JSONResponse({"error": "bot.py 不存在，无法触发重载"}, status_code=500)

    # ---- AI人设管理 ----
    # 优先跟随 aichat 插件的路径，否则用本地
    # 智能查找 persona_prompts.json（支持 site-packages 和本地安装）
    _PERSONA_PROMPTS_PATH = None
    _PERSONA_SEARCH_DIRS = []
    _persona_local_plugins = Path(__file__).parent.parent  # 本地 plugins 目录

    # 1) sys.modules 已加载的 aichat 模块
    for _mod_name in ("nonebot_plugin_aichat_baize", "src.plugins.nonebot_plugin_aichat_baize"):
        _mod = sys.modules.get(_mod_name)
        if _mod and hasattr(_mod, "__file__") and _mod.__file__:
            _d = Path(_mod.__file__).parent
            if _d not in _PERSONA_SEARCH_DIRS:
                _PERSONA_SEARCH_DIRS.append(_d)

    # 2) 从 aichat.config 模块直接拿路径（兼容 pip 和本地插件两种安装方式）
    try:
        from nonebot_plugin_aichat_baize.config import PERSONA_PROMPTS_FILE as _AICHAT_PERSONA_PATH
        _PERSONA_PROMPTS_PATH = _AICHAT_PERSONA_PATH
    except ImportError:
        try:
            from src.plugins.nonebot_plugin_aichat_baize.config import PERSONA_PROMPTS_FILE as _AICHAT_PERSONA_PATH
            _PERSONA_PROMPTS_PATH = _AICHAT_PERSONA_PATH
        except ImportError:
            pass

    # 3) find_spec 定位
    if not _PERSONA_PROMPTS_PATH:
        try:
            from importlib.util import find_spec
            for _spec_name in ("nonebot_plugin_aichat_baize", "src.plugins.nonebot_plugin_aichat_baize"):
                _spec = find_spec(_spec_name)
                if _spec and _spec.origin:
                    _d = Path(_spec.origin).parent
                    if _d not in _PERSONA_SEARCH_DIRS:
                        _PERSONA_SEARCH_DIRS.append(_d)
        except Exception:
            pass

    # 4) 本地目录查找
    for _sub in ("nonebot_plugin_aichat_baize", "nonebot_plugin_deepseek_chat/nonebot_plugin_aichat_baize"):
        _d = _persona_local_plugins / _sub
        if _d.is_dir() and _d not in _PERSONA_SEARCH_DIRS:
            _PERSONA_SEARCH_DIRS.append(_d)

    # 5) glob 兜底
    for _candidate in _persona_local_plugins.glob("**/persona_prompts.json"):
        _cand_dir = _candidate.parent
        if _cand_dir not in _PERSONA_SEARCH_DIRS:
            _PERSONA_SEARCH_DIRS.append(_cand_dir)

    # 在候选目录中查找 persona_prompts.json（含 data/ 子目录）
    if not _PERSONA_PROMPTS_PATH:
        for _search_dir in _PERSONA_SEARCH_DIRS:
            for _sub in ("", "data"):
                _candidate_path = _search_dir / _sub / "persona_prompts.json"
                if _candidate_path.is_file():
                    _PERSONA_PROMPTS_PATH = str(_candidate_path)
                    break
            else:
                continue
            break

    # 最终兜底：优先用已找到的 search dir，其次回退到 aichat 插件目录
    if not _PERSONA_PROMPTS_PATH:
        if _PERSONA_SEARCH_DIRS:
            _PERSONA_PROMPTS_PATH = str(_PERSONA_SEARCH_DIRS[0] / "persona_prompts.json")
        else:
            # 最后的回退：aichat 插件本地目录
            _PERSONA_PROMPTS_PATH = str(_persona_local_plugins / "nonebot_plugin_aichat_baize" / "persona_prompts.json")

    @app.get("/api/persona")
    async def get_persona():
        """读取 persona_prompts.json 返回完整人设数据"""
        if not os.path.exists(_PERSONA_PROMPTS_PATH):
            # 返回空白模板
            return {
                "persona_catalog": {
                    "1": {
                        "name": "默认人设",
                        "system_prompt": "你是一个友好的AI助手，请用中文回复。",
                        "display_model": "默认",
                        "description": "默认人设",
                    }
                },
                "hidden_persona_catalog": {},
                "hidden_persona_whitelists": {},
            }
        try:
            with open(_PERSONA_PROMPTS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 确保三个顶层 key 都存在
            data.setdefault("persona_catalog", {})
            data.setdefault("hidden_persona_catalog", {})
            data.setdefault("hidden_persona_whitelists", {})
            return data
        except Exception as e:
            logger.error(f"读取人设文件失败: {e}")
            return JSONResponse({"error": f"读取人设文件失败: {e}"}, status_code=500)

    @app.post("/api/persona/save")
    async def save_persona(request: Request):
        """保存人设数据到 persona_prompts.json"""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "请求体需为 JSON"}, status_code=400)

        # 基本校验
        required_keys = {"persona_catalog", "hidden_persona_catalog", "hidden_persona_whitelists"}
        if not isinstance(body, dict):
            return JSONResponse({"error": "数据格式错误，需为 JSON 对象"}, status_code=400)

        # 确保必要 key 存在
        for key in required_keys:
            if key not in body:
                body[key] = {}

        # 备份旧文件
        backup_path = _PERSONA_PROMPTS_PATH + ".bak"
        try:
            if os.path.exists(_PERSONA_PROMPTS_PATH):
                shutil.copy2(_PERSONA_PROMPTS_PATH, backup_path)
        except Exception as e:
            logger.warning(f"备份人设文件失败: {e}")

        try:
            with open(_PERSONA_PROMPTS_PATH, "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)
            logger.info("人设配置已通过 WebUI 保存")

            # 尝试通知 DeepSeek 对话插件重新加载人设
            reload_msg = ""
            try:
                for mod_name, mod in list(sys.modules.items()):
                    if hasattr(mod, "reload_personas") and callable(mod.reload_personas):
                        mod.reload_personas()
                        reload_msg = "，已自动重载插件人设"
                        logger.info(f"已触发插件 {mod_name} 的人设重载")
                        break
            except Exception as e:
                logger.warning(f"自动重载插件人设失败: {e}")

            return {"success": True, "message": f"人设配置已保存（旧文件已备份为 .bak）{reload_msg}"}
        except Exception as e:
            logger.error(f"保存人设文件失败: {e}")
            return JSONResponse({"error": f"保存失败: {e}"}, status_code=500)

    # ---- Token 用量统计 ----
    # 智能查找 token_daily.json：优先从 aichat 插件目录查找（支持 site-packages 和本地安装）
    _TOKEN_DAILY_PATH = None
    _TOKEN_DAILY_SEARCH_DIRS = []

    _local_plugins = Path(__file__).parent.parent

    # 1) 通过 sys.modules 查找已加载的 aichat 模块
    for _mod_name in ("nonebot_plugin_aichat_baize", "src.plugins.nonebot_plugin_aichat_baize"):
        _mod = sys.modules.get(_mod_name)
        if _mod and hasattr(_mod, "__file__") and _mod.__file__:
            _d = Path(_mod.__file__).parent
            if _d not in _TOKEN_DAILY_SEARCH_DIRS:
                _TOKEN_DAILY_SEARCH_DIRS.append(_d)

    # 2) 尝试直接 import（site-packages）
    try:
        import nonebot_plugin_aichat_baize
        _aichat_dir = Path(nonebot_plugin_aichat_baize.__file__).parent
        if _aichat_dir not in _TOKEN_DAILY_SEARCH_DIRS:
            _TOKEN_DAILY_SEARCH_DIRS.append(_aichat_dir)
    except Exception:
        pass

    # 3) find_spec 文件系统定位
    try:
        from importlib.util import find_spec as _find_spec
        for _spec_name in ("nonebot_plugin_aichat_baize", "src.plugins.nonebot_plugin_aichat_baize"):
            _spec = _find_spec(_spec_name)
            if _spec and _spec.origin:
                _d = Path(_spec.origin).parent
                if _d not in _TOKEN_DAILY_SEARCH_DIRS:
                    _TOKEN_DAILY_SEARCH_DIRS.append(_d)
    except Exception:
        pass

    # 4) 本地插件目录直接查找
    for _sub in ("nonebot_plugin_aichat_baize", "nonebot_plugin_deepseek_chat/nonebot_plugin_aichat_baize"):
        _d = _local_plugins / _sub
        if _d.is_dir() and _d not in _TOKEN_DAILY_SEARCH_DIRS:
            _TOKEN_DAILY_SEARCH_DIRS.append(_d)

    # 5) glob 兜底搜索
    for _candidate in _local_plugins.glob("**/token_daily.json"):
        _cand_dir = _candidate.parent
        if _cand_dir not in _TOKEN_DAILY_SEARCH_DIRS:
            _TOKEN_DAILY_SEARCH_DIRS.append(_cand_dir)

    # 在所有候选目录中查找 token_daily.json（含 data/ 子目录）
    for _search_dir in _TOKEN_DAILY_SEARCH_DIRS:
        for _sub in ("", "data"):
            _candidate_path = _search_dir / _sub / "token_daily.json"
            if _candidate_path.is_file():
                _TOKEN_DAILY_PATH = str(_candidate_path)
                break
        else:
            continue
        break

    @app.get("/api/token-stats")
    async def get_token_stats():
        """读取 token_daily.json，返回每日用量统计和汇总"""
        data = {}
        if os.path.exists(_TOKEN_DAILY_PATH):
            try:
                with open(_TOKEN_DAILY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        # 尝试从插件 CONFIG 读取 Token 定价
        input_price = 1.0 / 1_000_000   # 默认 DeepSeek
        output_price = 4.0 / 1_000_000
        try:
            plugin_py = os.path.join(os.path.dirname(os.path.dirname(__file__)) or ".", "deepseek对话PRO (1).py")
            if os.path.exists(plugin_py):
                with open(plugin_py, "r", encoding="utf-8") as f:
                    ptext = f.read()
                for key, default in [("INPUT_TOKEN_PRICE", None), ("OUTPUT_TOKEN_PRICE", None)]:
                    m = re.search(rf'"{key}"\s*:\s*(.+?)\s*,', ptext)
                    if m:
                        try:
                            val = float(eval(m.group(1).strip()))
                            if key == "INPUT_TOKEN_PRICE":
                                input_price = val
                            else:
                                output_price = val
                        except Exception:
                            pass
        except Exception:
            pass

        total_input = sum(d.get("input", 0) for d in data.values())
        total_output = sum(d.get("output", 0) for d in data.values())
        total_calls = sum(d.get("calls", 0) for d in data.values())
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_entry = data.get(today_str, {"input": 0, "output": 0, "calls": 0})

        daily = []
        from datetime import timedelta
        today = datetime.now().date()
        for i in range(13, -1, -1):
            d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            entry = data.get(d, {"input": 0, "output": 0, "calls": 0})
            daily.append({
                "date": d[5:],
                "input": entry.get("input", 0),
                "output": entry.get("output", 0),
                "calls": entry.get("calls", 0),
            })

        return {
            "summary": {
                "total_input": total_input,
                "total_output": total_output,
                "total_tokens": total_input + total_output,
                "total_calls": total_calls,
                "today_input": today_entry.get("input", 0),
                "today_output": today_entry.get("output", 0),
                "today_tokens": today_entry.get("input", 0) + today_entry.get("output", 0),
                "today_calls": today_entry.get("calls", 0),
                "total_cost": total_input * input_price + total_output * output_price,
                "today_cost": today_entry.get("input", 0) * input_price + today_entry.get("output", 0) * output_price,
            },
            "daily": daily,
        }

    # ---- 帮助模块管理 API（可选，兼容本地插件和 pip 安装） ----
    _HELP_AVAILABLE = False
    _help_router = None
    _help_data_dir = None
    for _help_mod in ("src.plugins.nonebot_plugin_help_baize", "nonebot_plugin_help_baize"):
        try:
            _help_mod_obj = __import__(f"{_help_mod}.webui_api", fromlist=["router"])
            _help_router = _help_mod_obj.webui_api.router
            _HELP_AVAILABLE = True
            # 定位 help 插件目录（用于挂载 data 静态资源）
            _help_init = __import__(_help_mod, fromlist=["__file__"])
            if hasattr(_help_init, "__file__") and _help_init.__file__:
                _help_data_dir = Path(_help_init.__file__).parent / "data"
            break
        except ImportError:
            continue
    if _HELP_AVAILABLE and _help_router:
        app.include_router(_help_router)
        if _help_data_dir and _help_data_dir.is_dir():
            app.mount("/help-data", StaticFiles(directory=str(_help_data_dir)), name="help_data")

    # 挂载 screenshots 目录（WebUI 截图/资源）
    _screenshots = Path(__file__).parent / "screenshots"
    if _screenshots.is_dir():
        app.mount("/screenshots", StaticFiles(directory=str(_screenshots)), name="screenshots")

    return app

