# python3
# -*- coding: utf-8 -*-
"""
Web UI 登录认证系统
提供基于 Token 的认证：登录、登出、密码修改、Token 校验
"""

import hashlib
import json
import secrets
import string as _string
import time
from pathlib import Path
from typing import TYPE_CHECKING

from nonebot import logger

if TYPE_CHECKING:
    from fastapi import Request

# 数据目录（独立定义，避免循环导入）
DATA_DIR = Path("data") / "web_ui"
DATA_DIR.mkdir(parents=True, exist_ok=True)

AUTH_FILE = DATA_DIR / "auth.json"
_active_tokens: dict = {}  # {token: expire_time}


def _hash_pw(password: str) -> str:
    return hashlib.sha256(f"lhcbot_webui_{password}".encode()).hexdigest()


def _gen_password(length: int = 10) -> str:
    chars = _string.ascii_letters + _string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def _load_auth(data_dir: Path = None) -> dict:
    """加载认证数据，首次启动生成默认账号"""
    auth_file = (data_dir / "auth.json") if data_dir else AUTH_FILE
    if auth_file.exists():
        try:
            return json.loads(auth_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    # 首次启动：使用默认密码
    pw = "admin"
    data = {
        "username": "admin",
        "password_hash": _hash_pw(pw),
        "first_login": True,
        "admins": [],  # 额外管理员 QQ 号列表
    }
    auth_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.warning("╔══════════════════════════════════════╗")
    logger.warning("║  Web UI 管理面板登录信息            ║")
    logger.warning(f"║  用户名: admin                      ║")
    logger.warning(f"║  密码:   {pw}                       ║")
    logger.warning("║  首次登录后建议修改密码            ║")
    logger.warning("╚══════════════════════════════════════╝")
    return data


def _save_auth(data: dict, data_dir: Path = None):
    """保存认证数据到文件"""
    auth_file = (data_dir / "auth.json") if data_dir else AUTH_FILE
    auth_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _verify_token(token: str) -> bool:
    """校验 Token 是否有效"""
    if token in _active_tokens:
        if time.time() < _active_tokens[token]:
            return True
        del _active_tokens[token]
    return False


def _check_auth(request: "Request") -> bool:
    """检查请求是否已认证（从 Header 或 Cookie 取 token）"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        token = request.cookies.get("lhc_token", "")
    return _verify_token(token)


# 模块加载时初始化认证数据
_auth_data = _load_auth()
