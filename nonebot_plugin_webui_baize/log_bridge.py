# python3
# -*- coding: utf-8 -*-
"""
共享日志桥接模块 — 在 bot.py 中最早导入，确保从启动第一刻起就捕获日志。
同时被 web_ui.py 引用，共享同一个 _log_buffer。
"""

import logging
import re
import sys
from datetime import datetime
from typing import Dict, List, Set

# ==================== 共享缓冲区 ====================
_log_buffer: List[Dict[str, str]] = []
MAX_LOG_BUFFER = 500

# 追踪启动阶段产生过 ERROR/CRITICAL 的模块名（用于插件健康检查）
_error_modules: Set[str] = set()
_error_tracking_frozen = False

# 匹配 NoneBot 插件导入失败日志：Failed to import "插件名" / Failed to load plugin "xxx"
_PLUGIN_FAIL_RE = re.compile(
    r'Failed to (?:load|import)\s+(?:plugin\s+)?["\'](.+?)["\']',
    re.IGNORECASE,
)


def _append_log(level: str, message: str) -> None:
    """向共享缓冲区追加一条日志"""
    _log_buffer.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "message": message,
    })
    if len(_log_buffer) > MAX_LOG_BUFFER:
        _log_buffer.pop(0)

    # 启动阶段错误追踪（冻结后不再追踪，避免运行时错误误判插件状态）
    if not _error_tracking_frozen and level in ("ERROR", "CRITICAL"):
        # 1) 从消息格式 `logger名 | 内容` 提取 logger 名
        if " | " in message:
            logger_name = message.split(" | ", 1)[0]
            _error_modules.add(logger_name)
        # 2) 正则匹配引号内的插件名（支持中文）
        m = _PLUGIN_FAIL_RE.search(message)
        if m:
            _error_modules.add(m.group(1))


def freeze_error_tracking():
    """冻结启动错误追踪：此后不再记录新的 ERROR 模块（避免运行时错误误判）"""
    global _error_tracking_frozen
    _error_tracking_frozen = True


def collect_logs(limit: int = 200) -> List[Dict[str, str]]:
    """返回缓冲区中最近 N 条日志"""
    return list(_log_buffer[-limit:])


# ==================== 指令使用统计 ====================

import json as _json
from collections import defaultdict
from datetime import date as _date
from pathlib import Path as _Path

# 统计数据持久化路径
_STATS_DIR = _Path(__file__).parent / "data"
_STATS_FILE = _STATS_DIR / "cmd_stats.json"
_SAVE_INTERVAL = 5  # 每 N 次记录后保存一次

_cmd_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
# 结构: {"复读禁言": {"on_command/开启复读禁言": 5, "on_fullmatch/扔漂流瓶": 3}}
_today_date = _date.today().isoformat()
_today_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
_save_counter = 0


def _check_today():
    """检查日期是否跨天，跨天则清零今日统计"""
    global _today_date, _today_usage
    today = _date.today().isoformat()
    if today != _today_date:
        _today_date = today
        _today_usage = defaultdict(lambda: defaultdict(int))


def _load_cmd_stats():
    """从磁盘加载统计记录（命令统计 + 消息计数 + 今日统计）"""
    global _cmd_usage, _msg_recv_count, _msg_sent_count, _today_date, _today_usage, _user_msg_counts
    try:
        if _STATS_FILE.exists():
            data = _json.loads(_STATS_FILE.read_text(encoding="utf-8"))
            # 命令统计（全部历史）
            raw = data.get("cmd_usage", {})
            _cmd_usage = defaultdict(lambda: defaultdict(int))
            for plugin, commands in raw.items():
                for cmd_full, count in commands.items():
                    _cmd_usage[plugin][cmd_full] = int(count)
            # 今日统计
            saved_date = data.get("today_date", "")
            saved_today = data.get("today_usage", {})
            if saved_date == _date.today().isoformat():
                _today_date = saved_date
                _today_usage = defaultdict(lambda: defaultdict(int))
                for plugin, commands in saved_today.items():
                    for cmd_full, count in commands.items():
                        _today_usage[plugin][cmd_full] = int(count)
            # 消息计数
            _msg_recv_count = int(data.get("msg_recv", 0))
            _msg_sent_count = int(data.get("msg_sent", 0))
            saved_users = data.get("user_msg_counts", {})
            _user_msg_counts = defaultdict(int, {k: int(v) for k, v in saved_users.items()})
    except Exception:
        pass


def _save_cmd_stats():
    """将统计记录写入磁盘"""
    try:
        _STATS_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "cmd_usage": {p: dict(cmds) for p, cmds in _cmd_usage.items() if cmds},
            "today_date": _today_date,
            "today_usage": {p: dict(cmds) for p, cmds in _today_usage.items() if cmds},
            "msg_recv": _msg_recv_count,
            "msg_sent": _msg_sent_count,
            "user_msg_counts": dict(_user_msg_counts),
        }
        _STATS_FILE.write_text(_json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


# ── 消息收发计数（持久化）──
_msg_recv_count = 0
_msg_sent_count = 0


def add_msg_recv(n: int = 1):
    global _msg_recv_count, _save_counter
    _msg_recv_count += n
    _save_counter += 1
    if _save_counter >= _SAVE_INTERVAL:
        _save_cmd_stats()
        _save_counter = 0


def add_msg_sent(n: int = 1):
    global _msg_sent_count, _save_counter
    _msg_sent_count += n
    _save_counter += 1
    if _save_counter >= _SAVE_INTERVAL:
        _save_cmd_stats()
        _save_counter = 0


def get_msg_counts() -> dict:
    return {"recv": _msg_recv_count, "sent": _msg_sent_count}


# ── 用户私聊消息计数（仅 Top 100，内存友好）──
_user_msg_counts: Dict[str, int] = defaultdict(int)


def add_user_msg(user_id: str):
    global _user_msg_counts
    _user_msg_counts[user_id] += 1
    # 超过 200 条记录时裁剪到 Top 100
    if len(_user_msg_counts) > 200:
        top = sorted(_user_msg_counts.items(), key=lambda x: x[1], reverse=True)[:100]
        _user_msg_counts = defaultdict(int, top)


def get_top_users(limit: int = 10) -> list:
    sorted_users = sorted(_user_msg_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"qq": uid, "count": cnt} for uid, cnt in sorted_users if cnt > 0]


def record_cmd_usage(plugin: str, cmd_type: str, trigger: str):
    """记录一次指令使用。cmd_type: on_command / on_fullmatch / on_message"""
    global _save_counter
    _check_today()
    key = f"{cmd_type}/{trigger}"
    _cmd_usage[plugin][key] += 1
    _today_usage[plugin][key] += 1
    _save_counter += 1
    if _save_counter >= _SAVE_INTERVAL:
        _save_cmd_stats()
        _save_counter = 0


def _usage_to_list(usage_dict: dict) -> list:
    """将 usage dict 转换为排序后的列表"""
    result = []
    for plugin, commands in usage_dict.items():
        for cmd_full, count in commands.items():
            parts = cmd_full.split("/", 1)
            cmd_type = parts[0] if len(parts) > 1 else ""
            trigger = parts[1] if len(parts) > 1 else cmd_full
            if count > 0:
                result.append({
                    "plugin": plugin,
                    "type": cmd_type,
                    "trigger": trigger,
                    "count": count,
                })
    result.sort(key=lambda x: x["count"], reverse=True)
    return result


def get_cmd_usage() -> list:
    """返回全部历史指令使用统计"""
    return _usage_to_list(_cmd_usage)


def get_cmd_usage_summary() -> dict:
    """返回汇总: {total, today, by_type, details, today_details}"""
    all_data = _usage_to_list(_cmd_usage)
    today_data = _usage_to_list(_today_usage)
    total = sum(d["count"] for d in all_data)
    today_total = sum(d["count"] for d in today_data)
    by_type = defaultdict(int)
    for d in all_data:
        by_type[d["type"]] += d["count"]
    return {
        "total": total,
        "today": today_total,
        "by_type": dict(by_type),
        "details": all_data[:50],
        "today_details": today_data[:20],
    }

# 启动时加载历史数据，关闭前保存
_load_cmd_stats()
import atexit as _atexit
_atexit.register(_save_cmd_stats)


def get_error_modules() -> Set[str]:
    """返回启动阶段产生过 ERROR/CRITICAL 的模块名集合"""
    return set(_error_modules)


# ==================== stdlib logging Handler ====================

class _EarlyLogHandler(logging.Handler):
    """标准 logging → 共享缓冲区"""

    SILENCED_LOGGERS = {
        "aiosqlite": logging.WARNING,
        "sqlalchemy": logging.WARNING,
        "asyncio": logging.WARNING,
        "urllib3": logging.WARNING,
        "httpx": logging.WARNING,
        "websockets": logging.WARNING,
    }

    def emit(self, record: logging.LogRecord):
        try:
            name = record.name
            if name.startswith(("uvicorn.", "fastapi.")) and record.levelno < logging.WARNING:
                return
            for silenced, min_level in self.SILENCED_LOGGERS.items():
                if name.startswith(silenced) and record.levelno < min_level:
                    return
            msg = record.getMessage()
            # 静音 NoneBot 事件处理的 DEBUG 日志（每条消息都输出，太吵）
            if name == "nonebot" and record.levelno < logging.INFO:
                if msg and "Processors" in msg:
                    return
            if msg and msg.strip():
                _append_log(record.levelname, f"{name} | {msg.strip()}")
        except Exception:
            self.handleError(record)


# ==================== 初始化 ====================

def setup():
    """初始化日志桥接（幂等，可多次调用）"""
    # --- stdlib logging ---
    root = logging.getLogger()
    if not any(isinstance(h, _EarlyLogHandler) for h in root.handlers):
        h = _EarlyLogHandler()
        h.setLevel(logging.INFO)
        root.addHandler(h)

    # --- loguru ---
    try:
        from nonebot import logger as nb_logger
    except ImportError:
        nb_logger = None

    if nb_logger is not None:
        sink_attr = "_log_bridge_sink_id"
        if not hasattr(setup, sink_attr):
            def _loguru_sink(message):
                try:
                    r = message.record
                    _append_log(r["level"].name, f"{r['name']} | {r['message']}")
                except Exception:
                    pass

            setattr(setup, sink_attr, nb_logger.add(
                _loguru_sink,
                level="DEBUG",
                format="{message}",
                catch=True,
            ))

    # --- stdout（捕获 print）---
    if not isinstance(sys.stdout, _StdoutRedirector):
        sys.stdout = _StdoutRedirector(sys.stdout, "INFO")


class _StdoutRedirector:
    """将 print() 输出重定向到 logging → 共享缓冲区"""
    def __init__(self, stream, level="INFO"):
        self._stream = stream
        self._level = level

    def write(self, s: str):
        if s:
            self._stream.write(s)
            self._stream.flush()
            line_logger = logging.getLogger("stdout")
            for line in s.splitlines():
                line = line.strip()
                if line:
                    (line_logger.error if self._level == "ERROR" else line_logger.info)(line)

    def flush(self):
        self._stream.flush()

    def __getattr__(self, name):
        return getattr(self._stream, name)
