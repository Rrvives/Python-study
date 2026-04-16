"""
Token / 请求用户解析：供导航 manifest 与管理类 API 复用。
"""
import json
import re
from typing import Any

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .models import ApiToken

_BEARER_RE = re.compile(r"^\s*Bearer\s+(\S+)\s*$", re.I)


def extract_bearer_token(request: HttpRequest) -> str | None:
    """从 Authorization 头解析 Bearer Token。"""
    raw = request.headers.get("Authorization") or ""
    m = _BEARER_RE.match(raw)
    return m.group(1) if m else None


def get_user_from_token(token: str):
    """根据 ApiToken.key 查找用户；无效则返回 None。"""
    if not token:
        return None
    row = ApiToken.objects.select_related("user").filter(key=token).first()
    if not row or not row.user.is_active:
        return None
    return row.user


def resolve_target_user(request: HttpRequest):
    """
    解析“业务用户”：
    1) 已登录 Session 用户
    2) Bearer Token 对应用户
    3) GET 请求可带 ?username= 便于联调（仅 manifest 等读接口建议使用）
    """
    if request.user.is_authenticated:
        return request.user

    bearer = extract_bearer_token(request)
    if bearer:
        user = get_user_from_token(bearer)
        if user:
            return user

    if request.method == "GET":
        username = request.GET.get("username", "").strip()
        if username:
            User = get_user_model()
            return User.objects.filter(username=username, is_active=True).first()

    return None


def parse_json_body(request: HttpRequest) -> dict[str, Any]:
    """解析 JSON 请求体；非法时返回空 dict。"""
    if not request.body:
        return {}
    try:
        data = json.loads(request.body.decode("utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
