# python3
# -*- coding: utf-8 -*-
"""
插件配置编辑器
提供插件配置解析、更新、指令触发词编辑等功能
"""

import ast
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Optional



def _is_external_plugin(file_path: Path) -> bool:
    """判断插件是否为 pip 安装的外部包（位于 site-packages）"""
    path_str = str(file_path.resolve())
    return ("site-packages" in path_str or "dist-packages" in path_str)


def _resolve_plugin_file(module: str) -> Optional[Path]:
    """定位插件的主 .py 文件（本地插件 + pip 外部插件）"""
    plugins_dir = Path(__file__).parent.parent  # 上一级是 plugins 目录
    # 1) 本地单文件: xxx.py
    f = (plugins_dir / f"{module}.py")
    if f.is_file():
        return f
    # 2) 本地目录包: xxx/__init__.py
    f = (plugins_dir / module / "__init__.py")
    if f.is_file():
        return f
    # 3) pip 安装的外部插件：先查 sys.modules，再 importlib，最后 find_spec
    try:
        mod = sys.modules.get(module)
        if mod is None:
            try:
                import importlib
                mod = importlib.import_module(module)
            except Exception:
                mod = None
        if mod is not None and hasattr(mod, "__file__") and mod.__file__:
            f = Path(mod.__file__)
            if f.is_file():
                return f
        # 已安装但未加载的包：用 find_spec 无导入定位
        from importlib.util import find_spec
        spec = find_spec(module)
        if spec is None:
            # 尝试连字符/下划线互换
            alt = module.replace("-", "_") if "-" in module else module.replace("_", "-")
            if alt != module:
                spec = find_spec(alt)
        if spec and spec.origin:
            f = Path(spec.origin)
            if f.is_file():
                return f
    except Exception:
        pass
    return None


_CONFIG_LINE_RE = re.compile(
    r'^(\s*)([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)(\s*#\s*(.*))?$'
)
_EXCLUDED_VARS = {
    "__plugin_meta__", "__all__", "__version__",
    "__author__", "__license__", "__copyright__",
}


def _parse_plugin_config(file_path: Path) -> list:
    """解析插件 .py 文件中的模块级配置常量（UPPER_CASE = value）+ CONFIG 字典内键值"""
    if not file_path.exists():
        return []
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    configs = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = _CONFIG_LINE_RE.match(line)
        if not m:
            continue
        name = m.group(2)
        if name in _EXCLUDED_VARS or name.startswith("_"):
            continue
        raw_value = m.group(3).strip().rstrip(",")

        # 特殊处理 CONFIG = { ... } 多行字典
        if name == "CONFIG" and raw_value == "{":
            dict_text = ""
            brace_depth = 0
            started = False
            for l in text.splitlines()[lineno - 1:]:
                dict_text += l + "\n"
                brace_depth += l.count("{") - l.count("}")
                if l.count("{") > 0:
                    started = True
                if started and brace_depth == 0:
                    break
            # 提取每行的行内注释
            key_comments = {}
            for l in dict_text.splitlines():
                cm = re.match(r'\s*"([^"]+)"\s*:.*?#\s*(.*)', l)
                if cm:
                    key_comments[cm.group(1)] = cm.group(2).strip()

            try:
                inner = dict_text.split("{", 1)[1].rsplit("}", 1)[0]
                # 移除行内注释后解析
                clean = re.sub(r'#.*$', '', inner, flags=re.MULTILINE)
                parsed = ast.literal_eval("{" + clean + "}")
            except Exception:
                parsed = {}
                for l in dict_text.splitlines():
                    km = re.match(r'\s*"([^"]+)"\s*:\s*(.+)$', l)
                    if not km:
                        continue
                    key = km.group(1)
                    vraw = km.group(2).strip()
                    # 移除行内注释
                    vraw = re.sub(r'#.*$', '', vraw).strip()
                    # 如果整行以逗号结尾，去掉
                    if vraw.endswith(","):
                        vraw = vraw[:-1].strip()
                    # 如果是 _env("K", default) 或 _api_env("K", default) 函数调用，提取第二个参数
                    env_m = re.match(r'_(?:api_)?env\s*\(\s*"[^"]*"\s*,\s*(.+)\)\s*$', vraw)
                    if env_m:
                        vraw = env_m.group(1).strip()
                    try:
                        parsed[key] = ast.literal_eval(vraw)
                    except Exception:
                        parsed[key] = vraw.strip().strip('"').strip("'")
            if isinstance(parsed, dict):
                for k, v in parsed.items():
                    display_name = f"CONFIG.{k}"
                    configs.append({
                        "name": display_name,
                        "value": v,
                        "raw_value": repr(v),
                        "type": type(v).__name__,
                        "comment": key_comments.get(k, ""),
                        "line": lineno,
                        "section": "CONFIG",
                        "config_key": k,
                    })
            continue

        if raw_value in ("[", "{", "("):
            continue
        if "(" in raw_value and ")" not in raw_value:
            continue
        if raw_value.endswith("(") or re.match(r'^\w+\(', raw_value):
            continue

        comment = (m.group(5) or "").strip()
        try:
            parsed = ast.literal_eval(raw_value)
        except (ValueError, SyntaxError, MemoryError):
            continue

        # 检测单行 CONFIG = {...} 字典，展开内部键值（兜底）
        if name == "CONFIG" and isinstance(parsed, dict):
            for k, v in parsed.items():
                display_name = f"CONFIG.{k}"
                configs.append({
                    "name": display_name,
                    "value": v,
                    "raw_value": repr(v),
                    "type": type(v).__name__,
                    "comment": "CONFIG 字典项",
                    "line": lineno,
                    "section": "CONFIG",
                    "config_key": k,
                })
        else:
            configs.append({
                "name": name,
                "value": parsed,
                "raw_value": raw_value,
                "type": type(parsed).__name__,
                "comment": comment,
                "line": lineno,
            })
    # 如果主文件是 __init__.py，同时扫描同目录下的 config.py
    if file_path.name == "__init__.py":
        _cp = file_path.parent / "config.py"
        if _cp.exists():
            try:
                _sub_configs = _parse_plugin_config(_cp)
                for _sc in _sub_configs:
                    if not any(c["name"] == _sc["name"] for c in configs):
                        _sc["_file"] = str(_cp)
                        configs.append(_sc)
            except Exception:
                pass

    return configs


def _update_plugin_config(file_path: Path, changes: dict) -> bool:
    """更新插件配置。普通变量: {NAME: val}, CONFIG键: {CONFIG.XXX: val}"""
    # CONFIG 键如果有子文件（config.py），写到子文件
    _config_changes = {k: v for k, v in changes.items() if k.startswith("CONFIG.")}
    if _config_changes:
        for _sub in ["config.py", "config/config.py"]:
            _cp = file_path.parent / _sub
            if _cp.exists() and _cp != file_path:
                return _update_plugin_config(_cp, changes)

    if not file_path.exists():
        return False
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return False

    # 分离 CONFIG 键和普通变量
    config_changes = {}
    normal_changes = {}
    for k, v in changes.items():
        if k.startswith("CONFIG."):
            config_changes[k[7:]] = v  # CONFIG.API_KEY → API_KEY
        else:
            normal_changes[k] = v

    # 处理 CONFIG 字典内的键
    if config_changes:
        for key, new_val in config_changes.items():
            if isinstance(new_val, str):
                # 先尝试 _(api_)env("K", "old") → _(api_)env("K", "new")
                p1 = re.sub(
                    rf'("{key}"\s*:\s*_(?:api_)?env\("[^"]*"\s*,\s*")[^"]*("\s*\)\s*,)',
                    rf'\g<1>{new_val}\2',
                    text, count=1
                )
                if p1 != text:
                    text = p1
                else:
                    # 普通字符串 "KEY": "old", → "KEY": "new",
                    text = re.sub(
                        rf'("{key}"\s*:\s*)"[^"]*"(\s*,)',
                        rf'\g<1>"{new_val}"\2',
                        text, count=1
                    )
            elif isinstance(new_val, bool):
                text = re.sub(
                    rf'("{key}"\s*:\s*)(True|False)(\s*,)',
                    rf'\g<1>{str(new_val)}\3',
                    text, count=1
                )
            elif isinstance(new_val, (int, float)):
                # 先尝试 _(api_)env("K", old_num) → _(api_)env("K", new_num)
                p1 = re.sub(
                    rf'("{key}"\s*:\s*_(?:api_)?env\("[^"]*"\s*,\s*)[\d.eE+\-*/]+(\s*\)\s*,)',
                    rf'\g<1>{new_val}\2',
                    text, count=1
                )
                if p1 != text:
                    text = p1
                else:
                    text = re.sub(
                        rf'("{key}"\s*:\s*)[\d.eE+\-*/]+(\s*,)',
                    rf'\g<1>{new_val}\2',
                    text, count=1
                )

    # 处理普通变量
    lines = text.splitlines()
    changed_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = _CONFIG_LINE_RE.match(line)
        if not m:
            continue
        name = m.group(2)
        if name in _EXCLUDED_VARS or name.startswith("_"):
            continue
        if name not in normal_changes:
            continue
        new_val = normal_changes[name]
        old_comment = m.group(4) or ""
        indent = m.group(1)
        if isinstance(new_val, str):
            val_str = repr(new_val)
        elif isinstance(new_val, bool):
            val_str = "True" if new_val else "False"
        elif isinstance(new_val, (int, float)):
            val_str = str(new_val)
        else:
            val_str = repr(new_val)
        lines[i] = f"{indent}{name} = {val_str}{old_comment}"
        changed_count += 1

    if changed_count == 0 and not config_changes:
        return False

    text = "\n".join(lines) if changed_count > 0 else text

    # 写入前备份
    backup = file_path.with_suffix(".py.bak")
    try:
        shutil.copy2(file_path, backup)
    except Exception:
        pass

    try:
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    except Exception:
        # 恢复备份
        if backup.exists():
            shutil.copy2(backup, file_path)
        return False


# ── dataclass config.py 解析（如 gpt_image_draw/config.py）──

_CONFIG_KW_RE = re.compile(
    r'^(\s*)(\w+)\s*=\s*(.+?)(,?)\s*(#\s*(.*))?$'
)


def _parse_config_py(file_path: Path) -> list:
    """解析 config.py 的配置项（构造函数参数 或 dataclass 字段默认值）"""
    if not file_path.exists():
        return []
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    configs = []
    in_block = False
    has_kwargs = False  # 构造函数是否有显式参数

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if '= ' in stripped and '(' in stripped and not stripped.startswith('#'):
            in_block = True
            # 跳过含 "." 的调用（如 Path.cwd()、datetime.now()），它们不是配置类
            class_name = stripped.split('(')[0].split('=')[-1].strip()
            if '.' in class_name:
                in_block = False
                continue
            # 检查是否空构造函数: CONFIG = ClassName()
            if stripped.rstrip().endswith('()'):
                in_block = False  # 不进入参数块
            continue
        if in_block and stripped.startswith(')'):
            break
        if not in_block:
            continue
        if not stripped or stripped.startswith('#'):
            continue
        m = _CONFIG_KW_RE.match(line)
        if not m:
            continue
        _, name, raw_value, comma, _, comment = m.groups()
        raw_value = raw_value.strip().rstrip(',')
        comment = (comment or '').strip()
        try:
            parsed = ast.literal_eval(raw_value)
            vtype = type(parsed).__name__
        except (ValueError, SyntaxError):
            # 尝试从 _(api_)env("KEY", default) 中提取默认值 —— 仅接受可 literal_eval 的字面量
            env_m = re.match(r'_(?:api_)?env\s*\(\s*"[^"]*"\s*,\s*(.+)\)\s*$', raw_value)
            if env_m:
                inner = env_m.group(1).strip()
                try:
                    parsed = ast.literal_eval(inner)
                    vtype = type(parsed).__name__
                except (ValueError, SyntaxError):
                    continue  # default 不是字面量（如 str(xxx) / 变量引用），不可编辑，跳过
            # 尝试从 Path(_(api_)env("KEY", default)) 中提取
            elif (path_env_m := re.match(r'Path\s*\(\s*_(?:api_)?env\s*\(\s*"[^"]*"\s*,\s*(.+)\)\s*\)\s*$', raw_value)):
                inner = path_env_m.group(1).strip()
                try:
                    parsed = ast.literal_eval(inner)
                    vtype = type(parsed).__name__
                except (ValueError, SyntaxError):
                    continue
            # 尝试从 Path("...") 中提取字符串
            elif (path_m := re.match(r'Path\s*\(\s*"([^"]*)"\s*\)\s*$', raw_value)):
                parsed = path_m.group(1)
                vtype = "str"
            else:
                continue  # 无法解析的表达式，跳过
        has_kwargs = True
        configs.append({
            "name": name,
            "value": parsed,
            "raw_value": raw_value,
            "type": vtype,
            "comment": comment,
            "line": lineno,
        })

    # 如果是空构造函数，回退解析 dataclass 字段定义
    if not has_kwargs and not configs:
        configs = _parse_dataclass_fields(text)

    return configs


_DATACLASS_FIELD_RE = re.compile(
    r'^\s+(\w+)\s*:\s*(.+?)\s*=\s*(.+)$'
)


def _parse_dataclass_fields(text: str) -> list:
    """从 dataclass 类定义中解析字段默认值"""
    configs = []
    in_class = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith('class ') and ':' in stripped:
            in_class = True
            continue
        if in_class and not stripped:
            continue
        if in_class and not line.startswith((' ', '\t')):
            break
        if not in_class:
            continue
        if stripped.startswith('#') or stripped.startswith('@'):
            continue
        m = _DATACLASS_FIELD_RE.match(line)
        if not m:
            continue
        name, type_hint, raw_val_line = m.groups()
        # 分离行尾注释
        raw_value = raw_val_line.strip().rstrip(',')
        comment = ""
        if "  # " in raw_value:
            raw_value, comment = raw_value.rsplit("  # ", 1)
            raw_value = raw_value.strip().rstrip(',')
        # 处理 field(default=xxx) / field(default_factory=xxx)
        if raw_value.startswith('field('):
            dm = re.search(r'(?:default|default_factory)\s*=\s*(.+)$', raw_value)
            if dm:
                inner = dm.group(1).strip()
                if inner.endswith(')'):
                    inner = inner[:-1].strip()
                if inner.endswith(','):
                    inner = inner[:-1].strip()
                raw_value = inner
            # default_factory=lambda: 是计算字段，不可编辑，跳过
            if raw_value.startswith('lambda:') or raw_value.startswith('lambda :'):
                continue

        # 解析值：先尝试 literal_eval，再尝试剥离 lambda
        parsed = None
        vtype = "str"
        for attempt in (raw_value, re.sub(r'^lambda:\s*', '', raw_value)):
            try:
                parsed = ast.literal_eval(attempt)
                vtype = type(parsed).__name__
                break
            except (ValueError, SyntaxError):
                continue
        # 复杂表达式（跨行 field() 等）：保留原始字符串以便编辑
        if parsed is None:
            if raw_value.startswith('field('):
                continue  # 跨行 field() 暂不支持
            parsed = raw_value
            vtype = "str"

        configs.append({
            "name": name,
            "value": parsed,
            "raw_value": raw_value,
            "type": vtype,
            "comment": comment,
            "line": lineno,
        })
    return configs


def _update_config_py(file_path: Path, changes: dict) -> bool:
    """更新 config.py 中的配置值（构造函数参数 或 dataclass 字段 + 扩展构造函数）"""
    if not file_path.exists():
        return False
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return False

    lines = text.splitlines()
    in_block = False
    changed = 0
    block_start = -1
    block_end = -1

    for i, line in enumerate(lines):
        stripped = line.strip()
        if '= ' in stripped and '(' in stripped and not stripped.startswith('#'):
            in_block = True
            block_start = i
            # 空构造函数: CONFIG = ClassName()
            # 跳过含 "." 的调用（如 Path.cwd()、datetime.now()），它们不是配置类
            if stripped.rstrip().endswith('()'):
                class_name = stripped.split('(')[0].split('=')[-1].strip()
                if '.' in class_name:
                    in_block = False
                    continue
                base_indent = line[:len(line) - len(line.lstrip())]
                kw_indent = base_indent + "    "
                config_name = stripped.split('=')[0].strip()
                # 构建新的参数行
                kw_lines = []
                for key, val in changes.items():
                    if isinstance(val, str):
                        vs = repr(val)
                    elif isinstance(val, bool):
                        vs = "True" if val else "False"
                    else:
                        vs = repr(val)
                    kw_lines.append(f"{kw_indent}{key}={vs},")
                # 替换空构造函数为多行形式
                new_block = [f"{base_indent}{config_name} = {class_name}("]
                new_block.extend(kw_lines)
                new_block.append(f"{base_indent})")
                lines[i:i+1] = new_block
                changed = len(changes)
            continue
        if in_block and stripped.startswith(')'):
            block_end = i
            break
        if not in_block:
            continue
        m = _CONFIG_KW_RE.match(line)
        if not m:
            continue
        _, name, orig_val, comma, _, _ = m.groups()
        if name not in changes:
            continue

        new_val = changes[name]
        if isinstance(new_val, str):
            val_str = repr(new_val)
        elif isinstance(new_val, bool):
            val_str = "True" if new_val else "False"
        elif isinstance(new_val, (int, float)):
            val_str = str(new_val)
        else:
            val_str = repr(new_val)

        # 保留原始的 _env() / Path() / Path(_env()) 包装
        orig_val = orig_val.strip().rstrip(',')
        env_m = re.match(r'_(?:api_)?env\s*\(\s*("[^"]*")\s*,\s*.+\)\s*$', orig_val)
        path_env_m = re.match(r'Path\s*\(\s*_(?:api_)?env\s*\(\s*("[^"]*")\s*,\s*.+\)\s*\)\s*$', orig_val)
        path_m = re.match(r'Path\s*\(\s*.+\)\s*$', orig_val)
        if path_env_m:
            val_str = f"Path(_env({path_env_m.group(1)}, {val_str}))"
        elif env_m:
            val_str = f"_env({env_m.group(1)}, {val_str})"
        elif path_m:
            val_str = f"Path({val_str})"

        # 检测原始行的 = 前后空格风格，保持一致
        eq_match = re.match(r'^(\s*\w+\s*)(=\s*)(.+)$', line)
        eq_style = eq_match.group(2) if eq_match else " = "

        old_comment = (m.group(6) or '').strip()
        comment_part = f"  # {old_comment}" if old_comment else ""
        comma_part = "," if (comma or not old_comment) else ""
        i_indent = line[:len(line) - len(line.lstrip())]
        lines[i] = f"{i_indent}{name}{eq_style}{val_str}{comma_part}{comment_part}"
        changed += 1

    if changed == 0:
        return False

    backup = file_path.with_suffix(".py.bak")
    try:
        shutil.copy2(file_path, backup)
    except Exception:
        pass
    try:
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    except Exception:
        if backup.exists():
            shutil.copy2(backup, file_path)
        return False


def _parse_plugin_config_full(file_path: Path) -> dict:
    """完整解析：Python 常量 + 关联的 JSON 配置文件 + 指令触发词 + config.py"""
    result = {"configs": [], "json_files": [], "matchers": [], "config_py": None}

    # --- Python 常量 + 指令触发词 ---
    if file_path.exists():
        result["configs"] = _parse_plugin_config(file_path)
        result["matchers"] = _parse_plugin_matchers(file_path)

    # --- 目录插件：扫描同目录下其他 .py 文件的常量 + 指令 ---
    plugin_dir = file_path.parent
    if file_path.name == "__init__.py":
        for sibling in sorted(plugin_dir.glob("*.py")):
            if sibling.name == "__init__.py" or sibling.name.startswith("_") or sibling.name == "config.py":
                continue
            try:
                result["configs"].extend(_parse_plugin_config(sibling))
                result["matchers"].extend(_parse_plugin_matchers(sibling))
            except Exception:
                pass
        for sub in sorted(plugin_dir.iterdir()):
            if not sub.is_dir() or sub.name.startswith("_") or sub.name.startswith("."):
                continue
            for py in sorted(sub.glob("*.py")):
                if py.name.startswith("_"):
                    continue
                try:
                    result["configs"].extend(_parse_plugin_config(py))
                    result["matchers"].extend(_parse_plugin_matchers(py))
                except Exception:
                    pass

    # --- 目录插件的 config.py ---
    config_py_path = file_path.parent / "config.py"
    if config_py_path.is_file() and config_py_path != file_path:
        config_items = _parse_config_py(config_py_path)
        if config_items:
            try:
                display_path = str(config_py_path.relative_to(Path.cwd()))
            except ValueError:
                display_path = str(config_py_path)  # 外部插件用绝对路径
            result["config_py"] = {
                "path": display_path,
                "items": config_items,
            }

    # --- 检测关联的 JSON 配置文件 ---
    plugin_dir = file_path.parent
    project_root = Path.cwd()  # bot.py 会把 CWD 设到项目根目录
    _JSON_FILE_RE = re.compile(
        r'([A-Z_]*FILE|[A-Z_]*PATH)\s*=\s*.+?["\']([^"\']+?\.json)["\']'
    )
    _seen_json_files = set()  # 去重

    # 收集要扫描的 .py 文件
    # 单文件插件：只扫自身；目录插件：扫 __init__.py + config.py + 同目录子模块
    _files_to_scan = []
    if file_path.exists():
        _files_to_scan.append(file_path)
        if file_path.name == "__init__.py":
            # config.py（aichat 的 JSON 引用都在这里）
            _cp = plugin_dir / "config.py"
            if _cp.is_file() and _cp != file_path:
                _files_to_scan.append(_cp)
            # 同目录下其他 .py 文件
            for _sibling in sorted(plugin_dir.glob("*.py")):
                if _sibling.name != "__init__.py" and not _sibling.name.startswith("_") and _sibling not in _files_to_scan:
                    _files_to_scan.append(_sibling)

    for _scan_file in _files_to_scan:
        try:
            text = _scan_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in _JSON_FILE_RE.finditer(text):
            json_rel = m.group(2)
            if json_rel in _seen_json_files:
                continue
            _seen_json_files.add(json_rel)
            # 按优先级查找：插件目录 → 项目根目录 → data/ 子目录
            json_path = None
            candidates = [
                plugin_dir / json_rel,
                project_root / json_rel,
                project_root / "data" / json_rel,
            ]
            for candidate in candidates:
                resolved = candidate.resolve()
                # 安全检查：必须在项目根目录或插件目录下
                if (resolved.parent == plugin_dir.resolve()
                        or str(plugin_dir.resolve()) in str(resolved.parent)
                        or str(project_root.resolve()) in str(resolved.parent)):
                    if resolved.exists():
                        json_path = resolved
                        break

            if json_path is None:
                continue
            try:
                json_display = str(json_path.relative_to(project_root))
            except ValueError:
                json_display = str(json_path)
            result["json_files"].append({
                "name": m.group(1),
                "path": json_display,
                "content": _read_json_file(json_path),
                "parsed": _load_json_safe(json_path),
            })
    return result


def _read_json_file(file_path: Path) -> str:
    """读取 JSON 文件原始内容"""
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _load_json_safe(file_path: Path) -> dict:
    """安全解析 JSON，返回 dict 或错误信息"""
    try:
        return {"data": json.loads(file_path.read_text(encoding="utf-8"))}
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e.msg} (第 {e.lineno} 行)"}
    except Exception as e:
        return {"error": f"读取失败: {e}"}


def _write_json_file(file_path: Path, content: str) -> bool:
    """写入 JSON 文件（先验证 JSON 格式，再备份写入）"""
    # 验证 JSON 格式
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        return False

    # 备份
    backup = file_path.with_suffix(".json.bak")
    try:
        shutil.copy2(file_path, backup)
    except Exception:
        pass

    try:
        file_path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        if backup.exists():
            shutil.copy2(backup, file_path)
        return False


# ==================== 指令触发词编辑器 ====================

_MATCHER_RE = re.compile(
    r'^(\s*)(\w+)\s*=\s*(on_command|on_fullmatch|on_startswith|on_regex|on_endswith)\s*\(\s*(?:\(\s*)?(?:r)?(["\'])(.+?)\4'
)

# 匹配元组触发词: ("词1", "词2", ...)
_MATCHER_TUPLE_RE = re.compile(
    r'^(\s*)(\w+)\s*=\s*(on_command|on_fullmatch|on_startswith|on_regex|on_endswith)\s*\(\s*\(\s*(?:r)?(["\'])(.+?)\4'
)

# 匹配 on_alconna(Alconna("词云",...))
_ALCONNA_VAR_RE = re.compile(r'^(\s*)(\w+)\s*=\s*on_alconna\s*\(')
_ALCONNA_START_RE = re.compile(r'Alconna\s*\(')
_ALCONNA_QUOTE_RE = re.compile(r'^\s*(["\'])(.+?)\1')

# 匹配函数体内嵌的命令元组: ("/xxx", "action")   — 见 gif.py 的 _extract_command 模式
_INLINE_CMD_TUPLE_RE = re.compile(
    r'^\s+\(\s*(["\'])(/.+?)\1\s*,\s*(["\'])(.+?)\3\s*\)(.*)$'
)


def _parse_plugin_matchers(file_path: Path) -> list:
    """解析插件中所有 matcher 注册，提取触发词（含 on_alconna 和函数体内嵌命令元组）"""
    if not file_path.exists():
        return []
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    lines = text.splitlines()
    matchers = []

    for lineno, line in enumerate(lines, start=1):
        # 1) 单触发词
        m = _MATCHER_RE.match(line)
        if m:
            _, var_name, matcher_type, _, trigger = m.groups()
            matchers.append({"variable": var_name, "type": matcher_type, "trigger": trigger, "line": lineno})
            continue
        # 2) 元组触发词
        m = _MATCHER_TUPLE_RE.match(line)
        if m:
            _, var_name, matcher_type, _, trigger = m.groups()
            tuple_match = re.search(r'\(\s*(["\'])(.+?)\1\s*,\s*(["\'])(.+?)\3', line)
            triggers = [trigger]
            if tuple_match:
                triggers = [tuple_match.group(2), tuple_match.group(4)]
            for t in triggers:
                matchers.append({"variable": var_name, "type": matcher_type, "trigger": t, "line": lineno})
            continue
        # 3) on_alconna：找到 Alconna("触发词")，跨行搜索
        am = _ALCONNA_VAR_RE.match(line)
        if am:
            var_name = am.group(2)
            found_alconna = False
            for offset in range(20):
                idx = lineno + offset
                if idx >= len(lines):
                    break
                sl = lines[idx].strip()
                if not found_alconna:
                    if _ALCONNA_START_RE.search(sl):
                        found_alconna = True
                    continue
                # 在 Alconna(...) 内部找第一个字符串字面量
                qm = _ALCONNA_QUOTE_RE.match(sl)
                if qm:
                    matchers.append({"variable": var_name, "type": "on_alconna", "trigger": qm.group(2), "line": lineno})
                    break
            continue
        # 4) 函数体内嵌命令元组: ("/xxx", "action") — on_message 插件的手动命令解析
        im = _INLINE_CMD_TUPLE_RE.match(line)
        if im:
            trigger = im.group(2)
            matchers.append({
                "variable": f"_inline:{lineno}:{trigger}",  # 唯一标识，用于后续更新定位
                "type": "on_message",
                "trigger": trigger,
                "line": lineno,
            })

    return matchers


def _update_matcher_trigger(file_path: Path, variable: str, new_trigger: str) -> bool:
    """更新指定变量的指令触发词（支持标准 matcher 和内嵌命令元组）"""
    if not file_path.exists():
        return False
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return False

    lines = text.splitlines()

    # ── 内嵌命令元组: variable 格式为 "_inline:<lineno>:<old_trigger>" ──
    if variable.startswith("_inline:"):
        parts = variable.split(":", 2)
        if len(parts) >= 3:
            old_trigger = parts[2]
            target_lineno = int(parts[1])
            idx = target_lineno - 1  # 转为 0-based 索引
            if 0 <= idx < len(lines):
                line = lines[idx]
                im = _INLINE_CMD_TUPLE_RE.match(line)
                if im:
                    # 保留原始缩进（regex 的 ^\s+ 使得 im.start()==0，需手动提取）
                    indent = line[:len(line) - len(line.lstrip())]
                    old_quote = im.group(1)
                    # 替换第一个字符串（触发词），保留 action 和尾部内容不变
                    action_quote = im.group(3)
                    action_val = im.group(4)
                    trailing = im.group(5)  # ), 后面的逗号、注释等
                    new_line = indent + f"({old_quote}{new_trigger}{old_quote}, {action_quote}{action_val}{action_quote}){trailing}"
                    lines[idx] = new_line
                    backup = file_path.with_suffix(".py.bak")
                    try:
                        shutil.copy2(file_path, backup)
                    except Exception:
                        pass
                    try:
                        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                        return True
                    except Exception:
                        if backup.exists():
                            shutil.copy2(backup, file_path)
                        return False
        return False

    # ── 标准 matcher: variable = on_command("xxx", ...) ──
    for i, line in enumerate(lines):
        m = _MATCHER_RE.match(line)
        if not m:
            continue
        if m.group(2) != variable:
            continue
        indent = m.group(1)
        matcher_type = m.group(3)
        quote = m.group(4)
        # 重建该行，保留后续参数
        rest = line[m.end():].strip()
        if rest.startswith(','):
            new_line = f'{indent}{variable} = {matcher_type}({quote}{new_trigger}{quote}{rest}'
        elif rest.startswith(')'):
            new_line = f'{indent}{variable} = {matcher_type}({quote}{new_trigger}{quote})'
        elif rest:
            new_line = f'{indent}{variable} = {matcher_type}({quote}{new_trigger}{quote}, {rest}'
        else:
            new_line = f'{indent}{variable} = {matcher_type}({quote}{new_trigger}{quote})'
        lines[i] = new_line

        # 备份
        backup = file_path.with_suffix(".py.bak")
        try:
            shutil.copy2(file_path, backup)
        except Exception:
            pass

        try:
            file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return True
        except Exception:
            if backup.exists():
                shutil.copy2(backup, file_path)
            return False

    return False

