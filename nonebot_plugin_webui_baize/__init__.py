# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/06/23
# @Author  : Baize
# @Email   : 2491434931@qq.com
# @File    : __init__.py
# @Software: Claude Code

"""
Web UI 管理面板插件
提供基于 Web 的机器人管理界面，支持：
- 系统状态监控（CPU、内存、运行时间、消息统计）
- 插件列表查看与管理
- 日志实时查看
- 已连接 Bot 信息查看
- 在线群聊/好友列表查看
"""

import asyncio
import json
import os
import platform
import socket
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

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

from nonebot import get_bots, get_driver, get_loaded_plugins, logger, on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

HAS_WEB = True
try:
    from fastapi import BackgroundTasks, FastAPI, Query, Request
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    import uvicorn
except ImportError:
    logger.warning("FastAPI/uvicorn 未安装，Web UI 功能不可用")
    HTMLResponse = None  # type: ignore
    FastAPI = None
    HAS_WEB = False

__plugin_meta__ = PluginMetadata(
    name="Web UI 管理面板",
    description="基于 Web 的机器人管理界面，支持状态监控、插件管理、日志查看等功能",
    usage=(
        "webui start 启动Web管理服务器\n"
        "webui stop 停止Web管理服务器\n"
        "webui status 查看Web服务器状态\n"
        "webui 获取Web管理面板访问地址\n"
    ),
    extra={"author": "lhc", "version": "1.0.0"},
)

# ==================== 全局状态 ====================
START_TIME = time.time()  # Bot 启动时间戳（用于计算运行时长）
web_server_task: Optional[asyncio.Task] = None  # Web 服务器异步任务句柄
web_app: Optional[FastAPI] = None  # FastAPI 应用实例
WEB_PORT = 8899  # Web UI 监听端口
WEB_HOST = '0.0.0.0'  # Web UI 监听地址（0.0.0.0=所有网卡）

DATA_DIR = Path(__file__).parent / "data"  # Web UI 数据目录（插件目录下）
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==================== 子模块导入 ====================

from .auth import _auth_data, _check_auth  # noqa: E402
from .app import create_app  # noqa: E402
from .config_editor import _get_all_plugin_dirs, _parse_plugin_matchers  # noqa: E402

# ==================== 日志收集器（委托给共享模块 log_bridge）====================

from .log_bridge import (  # noqa: E402
    add_msg_recv,
    add_msg_sent,
    add_user_msg,
    collect_logs as _collect_logs,
    freeze_error_tracking,
    get_cmd_usage_summary,
    get_error_modules,
    get_msg_counts,
    get_top_users,
    record_cmd_usage,
    setup as _setup_log_bridge,
)


# ==================== 服务器管理 ====================

def _is_port_in_use(host: str, port: int) -> bool:
    """检查指定端口是否在监听"""
    try:
        if host == "0.0.0.0":
            # 0.0.0.0 绑定到所有接口，用 127.0.0.1 检测
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                return s.connect_ex(("127.0.0.1", port)) == 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False


async def _start_web_server() -> bool:
    """启动 Web 服务器，返回是否成功"""
    global web_server_task, web_app

    if web_server_task and not web_server_task.done():
        logger.info("Web 服务器已在运行中，跳过启动")
        return True

    # 先检查端口是否被占用
    if _is_port_in_use(WEB_HOST, WEB_PORT):
        logger.error(f"端口 {WEB_PORT} 已被占用，无法启动 Web UI")
        return False

    try:
        web_app = create_app(start_time=START_TIME, data_dir=DATA_DIR)
    except Exception as e:
        logger.error(f"创建 FastAPI 应用失败: {e}")
        return False

    config = uvicorn.Config(
        web_app,
        host=WEB_HOST,
        port=WEB_PORT,
        log_level="info",
        access_log=False,
        loop="asyncio",
    )
    server = uvicorn.Server(config)

    async def run_server():
        try:
            logger.info(f"Web UI 正在启动: http://{WEB_HOST}:{WEB_PORT}")
            await server.serve()
        except asyncio.CancelledError:
            logger.info("Web UI 服务器收到取消信号，正在关闭...")
            await server.shutdown()
            raise
        except Exception as e:
            logger.error(f"Web UI 服务器异常: {e}\n{traceback.format_exc()}")

    web_server_task = asyncio.ensure_future(run_server())

    # 等待服务器绑定端口（最多等待 3 秒）
    for _ in range(30):
        await asyncio.sleep(0.1)
        if _is_port_in_use(WEB_HOST, WEB_PORT):
            logger.success(f"✅ Web UI 服务器已启动: http://127.0.0.1:{WEB_PORT}")
            return True

    # 超时检查：task 是否已经异常退出
    if web_server_task.done():
        exc = web_server_task.exception()
        if exc:
            logger.error(f"Web 服务器启动失败: {exc}")
        else:
            logger.error("Web 服务器启动后立即退出（端口是否被占用？）")
        web_server_task = None
        web_app = None
        return False

    logger.warning(f"Web UI 可能未成功绑定端口 {WEB_PORT}，请检查网络配置")
    return True


async def _stop_web_server():
    """停止 Web 服务器"""
    global web_server_task, web_app
    if web_server_task and not web_server_task.done():
        web_server_task.cancel()
        try:
            await web_server_task
        except asyncio.CancelledError:
            pass
        web_server_task = None
        web_app = None
        logger.info("Web UI 服务器已停止")


def _get_server_status() -> str:
    """获取服务器状态描述"""
    if web_server_task is None:
        return "⚪ Web 服务器未启动"
    if web_server_task.done():
        return "🔴 Web 服务器已异常退出"
    return f"🟢 Web 服务器运行中\n📡 地址: http://127.0.0.1:{WEB_PORT}"


# ==================== NoneBot 指令 ====================

webui_start = on_command("webui", aliases={"webui start", "WebUI", "web界面"}, permission=SUPERUSER, priority=5, block=True)


@webui_start.handle()
async def webui_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    sub_cmd = args.extract_plain_text().strip().lower()

    if sub_cmd in ("stop", "停止", "关闭"):
        await _stop_web_server()
        await webui_start.finish("✅ Web 服务器已停止")
        return

    if sub_cmd in ("status", "状态"):
        status_text = _get_server_status()
        await webui_start.finish(status_text)
        return

    # 默认：启动
    if not HAS_WEB:
        await webui_start.finish("❌ FastAPI/uvicorn 未安装，无法启动 Web UI\n请执行: pip install fastapi uvicorn")
        return

    success = await _start_web_server()
    if success:
        await webui_start.finish(
            f"🌐 Web UI 管理面板已启动！\n"
            f"📡 访问地址: http://127.0.0.1:{WEB_PORT}\n"
            f"🔒 仅限本地访问，如需远程请修改 WEB_HOST"
        )
    else:
        await webui_start.finish(
            f"❌ Web UI 启动失败！\n"
            f"可能原因：端口 {WEB_PORT} 被占用、FastAPI/uvicorn 版本不兼容\n"
            f"请检查 Bot 控制台日志获取详细错误信息"
        )


# ==================== 消息/指令统计器 ====================

from nonebot import on_message as _on_message_hook
from nonebot.adapters.onebot.v11.event import MessageEvent as _MessageEvent
from nonebot.adapters.onebot.v11.bot import Bot as _Bot
from nonebot.message import event_preprocessor

# ── 消息接收计数器 ──
_stat_recv = _on_message_hook(priority=1, block=False)


@_stat_recv.handle()
async def _count_recv(event: _MessageEvent):
    add_msg_recv()
    # 私聊消息：按用户统计
    if not hasattr(event, 'group_id') or not event.group_id:
        add_user_msg(str(event.user_id))


# ── 消息发送计数器（包装 call_api）──
_original_bot_call_api = _Bot.call_api


async def _patched_bot_call_api(self, api: str, **data):
    if api in ("send_msg", "send_private_msg", "send_group_msg", "send_group_forward_msg"):
        add_msg_sent()
    return await _original_bot_call_api(self, api, **data)


_Bot.call_api = _patched_bot_call_api

# ── 指令使用自动追踪（event_preprocessor 在所有 matcher 之前运行）──
_cmd_trigger_map: dict = {}  # {trigger_text: (module, cmd_type)}
_cmd_start = "/"  # 默认 command_start


def _build_trigger_map():
    """扫描所有已加载插件（含目录插件），构建指令触发词查找表"""
    _cmd_trigger_map.clear()
    all_plugin_dirs = _get_all_plugin_dirs()

    def _scan_file(file_path: Path, module_name: str):
        try:
            matchers = _parse_plugin_matchers(file_path)
        except Exception:
            return
        for m in matchers:
            _cmd_trigger_map[m["trigger"]] = (module_name, m["type"])

    # 遍历所有插件目录
    for plugins_dir in all_plugin_dirs:
        # 单文件插件
        for f in sorted(plugins_dir.glob("*.py")):
            if not f.name.startswith("_"):
                _scan_file(f, f.stem)

        # 目录插件
        for d in sorted(plugins_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
                continue
            init_file = d / "__init__.py"
            if init_file.is_file():
                _scan_file(init_file, d.name)


_build_trigger_map()
logger.info(f"📊 指令统计触发词表已构建: {len(_cmd_trigger_map)} 个触发词")


@event_preprocessor
async def _track_cmd_usage(event):
    """在所有 matcher 之前运行，不受 block=True 影响"""
    try:
        text = event.get_plaintext().strip()
    except Exception:
        return
    if not text:
        return

    # 1) on_fullmatch：消息完全等于触发词（如 "捞漂流瓶"、"扔漂流瓶"）
    if text in _cmd_trigger_map:
        module, ctype = _cmd_trigger_map[text]
        if ctype in ("on_fullmatch", "on_command"):
            record_cmd_usage(module, ctype, text)
            return

    # 2) on_command：消息以 / 开头
    if text.startswith(_cmd_start):
        cmd_text = text[len(_cmd_start):].split()[0]
        if cmd_text in _cmd_trigger_map:
            module, ctype = _cmd_trigger_map[cmd_text]
            record_cmd_usage(module, ctype, cmd_text)
            return

    # 3) on_message：需要插件自行调用 record_cmd_usage()，不做自动检测


# ==================== 指令使用统计查询 ====================

_stats_cmd = on_command("指令使用统计", aliases={"历史指令统计", "指令统计"}, permission=SUPERUSER, priority=5, block=True)
_today_stats_cmd = on_command("今日指令使用统计", aliases={"今日指令统计", "今日统计"}, permission=SUPERUSER, priority=5, block=True)


def _build_stats_forward_node(bot_id: int, nickname: str, content: str) -> dict:
    """构建统计消息的合并转发节点"""
    try:
        seg = MessageSegment.node_custom(
            user_id=bot_id, nickname=nickname,
            content=Message(MessageSegment.text(content))
        )
        data = seg.data if isinstance(seg.data, dict) else {}
        if data:
            return {"type": "node", "data": data}
    except Exception:
        pass
    return {
        "type": "node",
        "data": {"uin": bot_id, "name": nickname, "user_id": bot_id, "nickname": nickname,
                 "content": Message(MessageSegment.text(content))},
    }


def _render_stats_as_nodes(bot_id: int, nickname: str, title: str, details: list) -> list:
    """将统计数据渲染为合并转发节点列表"""
    nodes = []
    # 标题节点
    total_count = sum(d["count"] for d in details)
    header = f"📊 {title}\n共 {total_count} 次使用，{len(details)} 个指令\n" + "─" * 20
    nodes.append(_build_stats_forward_node(bot_id, nickname, header))

    # 按使用次数降序
    sorted_details = sorted(details, key=lambda d: d["count"], reverse=True)
    # 分页：每页最多 15 条
    page_size = 15
    for i in range(0, len(sorted_details), page_size):
        chunk = sorted_details[i:i + page_size]
        lines = []
        for d in chunk:
            lines.append(f"🔹 /{d['trigger']} ({d['module']}) — {d['count']} 次")
        nodes.append(_build_stats_forward_node(bot_id, nickname, "\n".join(lines)))

    return nodes


@_stats_cmd.handle()
async def handle_cmd_stats(bot: Bot, event: MessageEvent):
    """历史指令使用统计"""
    summary = get_cmd_usage_summary()
    if not summary:
        await _stats_cmd.finish("📊 暂无指令使用记录")
        return

    details = []
    for item in summary:
        details.append({
            "trigger": item.get("trigger", "?"),
            "module": item.get("module", "?"),
            "count": item.get("count", 0),
        })

    bot_id = int(bot.self_id)
    nickname = "Bot 统计"
    nodes = _render_stats_as_nodes(bot_id, nickname, "📊 历史指令使用统计", details)

    if hasattr(event, 'group_id') and event.group_id:
        await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=nodes)
    else:
        await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=nodes)


@_today_stats_cmd.handle()
async def handle_today_stats(bot: Bot, event: MessageEvent):
    """今日指令使用统计"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    summary = get_cmd_usage_summary()
    details = []
    for item in summary:
        daily = item.get("daily", {})
        today_count = daily.get(today_str, 0)
        if today_count > 0:
            details.append({
                "trigger": item.get("trigger", "?"),
                "module": item.get("module", "?"),
                "count": today_count,
            })

    if not details:
        await _today_stats_cmd.finish(f"📊 {today_str} 暂无指令使用记录")

    bot_id = int(bot.self_id)
    nickname = "Bot 统计"
    nodes = _render_stats_as_nodes(bot_id, nickname, f"📊 今日指令使用统计 ({today_str})", details)

    if hasattr(event, 'group_id') and event.group_id:
        await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=nodes)
    else:
        await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=nodes)


# ==================== 日志查询指令 ====================

_log_cmd = on_command("日志", aliases={"查看日志", "bot日志", "Bot日志"}, permission=SUPERUSER, priority=5, block=True)


@_log_cmd.handle()
async def handle_log(bot: Bot, event: MessageEvent):
    """查看最近日志"""
    logs = _collect_logs()
    if not logs:
        await _log_cmd.finish("📋 暂无日志记录")
        return

    # 获取最近 100 条日志
    recent = logs[-100:]
    lines = ["📋 最近日志 (最新在上):", "─" * 30]
    for entry in reversed(recent):
        ts = entry.get("time", "?")
        level = entry.get("level", "INFO")
        msg = entry.get("message", "")
        emoji = {"ERROR": "🔴", "WARNING": "🟡", "SUCCESS": "🟢", "INFO": "🔵", "DEBUG": "⚪"}.get(level, "⚪")
        lines.append(f"{emoji} [{ts}] [{level}] {msg[:200]}")

    full_text = "\n".join(lines)
    bot_id = int(bot.self_id)
    nickname = "Bot 日志"
    nodes = [
        _build_stats_forward_node(bot_id, nickname, full_text),
    ]

    if hasattr(event, 'group_id') and event.group_id:
        await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=nodes)
    else:
        await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=nodes)


# ==================== 自动启动 ====================

driver = get_driver()

# 尽早注册日志桥接，确保启动器日志能被 Web UI 捕获
_setup_log_bridge()


@driver.on_startup
async def _auto_start_webui():
    """Bot 启动时自动启动 Web UI"""
    # 再次确认日志桥接已注册（热重载场景）
    _setup_log_bridge()
    if HAS_WEB:
        asyncio.ensure_future(_delayed_start())


async def _delayed_start():
    """延迟 2 秒启动，等待其他插件加载完成"""
    await asyncio.sleep(2)
    ok = await _start_web_server()
    if ok:
        logger.success(f"🌐 Web UI 已自动启动: http://127.0.0.1:{WEB_PORT}")
        # 启动阶段结束，冻结错误追踪（避免运行时错误误判插件加载失败）
        freeze_error_tracking()
    else:
        logger.warning(f"Web UI 自动启动失败，请发送「webui」手动启动")
