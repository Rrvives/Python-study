"""
用户管理、角色（Django Group）、动态路由权限等 JSON API。
需 staff 或 superuser + 有效 Bearer Token（登录接口除外）。
"""
import secrets
from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .auth_support import extract_bearer_token, get_user_from_token, parse_json_body
from .models import (
    ApiToken,
    ExtraRoute,
    ManagedMenu,
    MenuExtraItem,
    NavigationConfig,
)


def _json_error(message: str, status: int = 400):
    return JsonResponse({"message": message}, status=status)


def _require_staff_api_user(request):
    """返回已通过 Token/Session 鉴权且具备后台管理权限的用户。"""
    token = extract_bearer_token(request)
    user = get_user_from_token(token) if token else None
    if not user and request.user.is_authenticated:
        user = request.user
    if not user or not user.is_active:
        return None, _json_error("未登录或登录已失效", 401)
    if not (user.is_staff or user.is_superuser):
        return None, _json_error("需要管理员权限（is_staff）", 403)
    return user, None


def staff_api(view_func):
    """装饰器：校验 staff + JSON 响应错误。"""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user, err = _require_staff_api_user(request)
        if err:
            return err
        request.api_user = user  # type: ignore[attr-defined]
        return view_func(request, *args, **kwargs)

    return _wrapped


def superuser_api(view_func):
    """装饰器：仅超级管理员可访问。"""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user, err = _require_staff_api_user(request)
        if err:
            return err
        if not user.is_superuser:
            return _json_error("仅超级管理员可进行菜单配置", 403)
        request.api_user = user  # type: ignore[attr-defined]
        return view_func(request, *args, **kwargs)

    return _wrapped


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def auth_login(request):
    """POST /api/auth/login — 校验用户名密码，签发 Bearer Token。"""
    if request.method == "OPTIONS":
        return JsonResponse({})

    body = parse_json_body(request)
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    if not username or not password:
        return _json_error("用户名与密码不能为空", 400)

    # 首次启动时若系统中还没有账号，直接返回可执行的初始化指引。
    User = get_user_model()
    if not User.objects.filter(is_active=True).exists():
        return _json_error(
            "系统暂无可登录用户，请先在后端执行 `python manage.py createsuperuser` 创建管理员账号",
            400,
        )

    user = authenticate(request, username=username, password=password)
    if not user or not user.is_active:
        return _json_error("用户名或密码错误", 401)

    # 轮换 token：避免旧客户端长期持有同一密钥
    with transaction.atomic():
        ApiToken.objects.filter(user=user).delete()
        key = secrets.token_urlsafe(48)
        ApiToken.objects.create(user=user, key=key)

    display = (user.get_full_name() or "").strip() or user.username
    return JsonResponse(
        {
            "accessToken": key,
            "username": user.username,
            "displayName": display,
            # 前端可用于控制「创建 staff」等敏感项展示
            "isSuperuser": user.is_superuser,
            "isStaff": user.is_staff,
        }
    )


@csrf_exempt
@staff_api
@require_GET
def groups_list(request):
    """GET /api/groups — 角色列表（Django Group）。"""
    return JsonResponse({"groups": []})


def _normalize_group_ids(raw) -> list[int] | None:
    if raw is None:
        return []
    if not isinstance(raw, list):
        return None
    out: list[int] = []
    for x in raw:
        try:
            out.append(int(x))
        except (TypeError, ValueError):
            return None
    return out


@csrf_exempt
@staff_api
@require_http_methods(["GET", "POST", "OPTIONS"])
def users_collection(request):
    """
    GET /api/users — 用户列表。
    POST /api/users — 新建用户并设置密码。
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method == "GET":
        User = get_user_model()
        qs = User.objects.all().order_by("id").prefetch_related("groups")
        users = []
        for u in qs:
            users.append(
                {
                    "id": u.id,
                    "username": u.username,
                    "email": u.email or "",
                    "is_active": u.is_active,
                    "is_staff": u.is_staff,
                    "is_superuser": u.is_superuser,
                }
            )
        return JsonResponse({"users": users})

    body = parse_json_body(request)
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    email = (body.get("email") or "").strip()
    if not username or not password:
        return _json_error("username 与 password 必填", 400)

    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return _json_error("用户名已存在", 409)

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False,
            )
    except ValidationError as exc:
        return _json_error("; ".join(exc.messages), 400)

    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
        },
        status=201,
    )


@csrf_exempt
@staff_api
@require_http_methods(["PATCH", "OPTIONS"])
def users_patch(request, user_id: int):
    """PATCH /api/users/<id> — 更新密码、启用状态。"""
    if request.method == "OPTIONS":
        return JsonResponse({})

    User = get_user_model()
    user = User.objects.filter(id=user_id).first()
    if not user:
        return _json_error("用户不存在", 404)

    api_user = request.api_user  # type: ignore[attr-defined]
    if user.is_superuser and not api_user.is_superuser:
        return _json_error("无权修改超级用户", 403)

    body = parse_json_body(request)
    if user.is_superuser:
        # 规则：超级管理员账号只允许修改密码。
        forbidden = set(body.keys()) - {"password"}
        if forbidden:
            return _json_error("超级管理员仅允许修改密码", 403)

    if "password" in body:
        pwd = body.get("password") or ""
        if not pwd:
            return _json_error("password 不能为空字符串", 400)
        try:
            validate_password(pwd, user)
        except ValidationError as exc:
            return _json_error("; ".join(exc.messages), 400)
        user.set_password(pwd)

    if "is_active" in body:
        user.is_active = bool(body.get("is_active"))

    user.save()
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    )


def _active_navigation_config():
    return (
        NavigationConfig.objects.prefetch_related(
            "extra_routes__allowed_groups",
            "menu_extra_items__allowed_groups",
            "managed_menus__allowed_users",
            "managed_menus__parent",
        )
        .filter(is_active=True)
        .first()
    )


def _ensure_active_navigation_config():
    """
    若不存在启用配置则创建默认配置，避免菜单管理页首次进入时报 404。
    """
    config = _active_navigation_config()
    if config:
        return config
    return NavigationConfig.objects.create(version="server-auto", is_active=True)


def _parse_optional_int(raw):
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _normalize_user_ids(raw) -> list[int] | None:
    return _normalize_group_ids(raw)


def _validate_parent_menu(config: NavigationConfig, parent_id):
    if parent_id is None:
        return None, None
    parent_pk = _parse_optional_int(parent_id)
    if parent_pk is None:
        return None, _json_error("parent_id 需为整数或 null", 400)
    parent = ManagedMenu.objects.filter(id=parent_pk, config=config).first()
    if not parent:
        return None, _json_error("父级菜单不存在", 404)
    if parent.parent_id:
        return None, _json_error("仅支持两级菜单：二级菜单不能再挂子级", 400)
    return parent, None


@csrf_exempt
@staff_api
@require_http_methods(["GET", "PATCH", "OPTIONS"])
def user_menu_permissions(request, user_id: int):
    """
    GET /api/users/<id>/menu-permissions
    PATCH /api/users/<id>/menu-permissions
    在用户管理中按“用户”分配 managed_menu 显示权限。
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    User = get_user_model()
    target_user = User.objects.filter(id=user_id).first()
    if not target_user:
        return _json_error("用户不存在", 404)

    api_user = request.api_user  # type: ignore[attr-defined]
    if target_user.is_superuser:
        if request.method == "PATCH":
            return _json_error("超级管理员仅允许修改密码", 403)
        if not api_user.is_superuser:
            return _json_error("无权查看超级用户菜单权限", 403)

    config = _active_navigation_config()
    if not config:
        return JsonResponse(
            {
                "configVersion": None,
                "selectedMenuIds": [],
                "items": [],
            }
        )

    menus = list(
        ManagedMenu.objects.filter(config=config)
        .select_related("parent")
        .order_by("sort", "id")
    )

    if request.method == "GET":
        selected_ids = list(
            ManagedMenu.objects.filter(config=config, allowed_users=target_user).values_list(
                "id", flat=True
            )
        )
        items = []
        for row in menus:
            items.append(
                {
                    "id": row.id,
                    "menuKey": row.menu_key,
                    "label": row.label,
                    "parentId": row.parent_id,
                    "parentKey": row.parent.menu_key if row.parent else None,
                    "level": 1 if row.parent_id is None else 2,
                    "sort": row.sort,
                    "isEnabled": row.is_enabled,
                }
            )
        return JsonResponse(
            {
                "configVersion": config.version,
                "selectedMenuIds": selected_ids,
                "items": items,
            }
        )

    body = parse_json_body(request)
    menu_ids = body.get("menu_ids")
    if not isinstance(menu_ids, list):
        return _json_error("menu_ids 须为整数数组", 400)
    normalized = _normalize_user_ids(menu_ids)
    if normalized is None:
        return _json_error("menu_ids 须为整数数组", 400)

    menu_id_set = set(normalized)
    valid_menu_ids = {row.id for row in menus}
    if not menu_id_set.issubset(valid_menu_ids):
        return _json_error("包含无效 menu_ids（不属于当前导航配置）", 400)

    for row in menus:
        if row.id in menu_id_set:
            row.allowed_users.add(target_user)
        else:
            row.allowed_users.remove(target_user)

    return JsonResponse(
        {
            "userId": target_user.id,
            "selectedMenuIds": sorted(menu_id_set),
        }
    )


@csrf_exempt
@superuser_api
@require_http_methods(["GET", "POST", "OPTIONS"])
def managed_menus_collection(request):
    """
    GET /api/navigation/managed-menus
    POST /api/navigation/managed-menus
    仅超级管理员可维护一级/二级菜单及分配可见用户。
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    config = _ensure_active_navigation_config()

    if request.method == "GET":
        rows = (
            ManagedMenu.objects.filter(config=config)
            .select_related("parent")
            .prefetch_related("allowed_users")
            .order_by("sort", "id")
        )
        items = []
        for row in rows:
            items.append(
                {
                    "id": row.id,
                    "menuKey": row.menu_key,
                    "label": row.label,
                    "path": row.path,
                    "componentKey": row.component_key,
                    "parentId": row.parent_id,
                    "parentKey": row.parent.menu_key if row.parent else None,
                    "level": 1 if row.parent_id is None else 2,
                    "sort": row.sort,
                    "isEnabled": row.is_enabled,
                    "allowedUserIds": list(
                        row.allowed_users.values_list("id", flat=True)
                    ),
                }
            )
        return JsonResponse({"configVersion": config.version, "items": items})

    body = parse_json_body(request)
    menu_key = (body.get("menu_key") or "").strip()
    label = (body.get("label") or "").strip()
    path = (body.get("path") or "").strip()
    component_key = (body.get("component_key") or "").strip()
    sort = _parse_optional_int(body.get("sort"))
    is_enabled = bool(body.get("is_enabled", True))
    user_ids = _normalize_user_ids(body.get("allowed_user_ids"))
    parent, parent_err = _validate_parent_menu(config, body.get("parent_id"))

    if not menu_key or not label:
        return _json_error("menu_key 与 label 必填", 400)
    if sort is None:
        sort = 0
    if user_ids is None:
        return _json_error("allowed_user_ids 须为整数数组", 400)
    if parent_err:
        return parent_err
    if ManagedMenu.objects.filter(config=config, menu_key=menu_key).exists():
        return _json_error("menu_key 已存在", 409)

    row = ManagedMenu.objects.create(
        config=config,
        parent=parent,
        menu_key=menu_key,
        label=label,
        path=path,
        component_key=component_key,
        sort=sort,
        is_enabled=is_enabled,
    )
    users = list(get_user_model().objects.filter(id__in=user_ids or []))
    row.allowed_users.set(users)
    return JsonResponse(
        {
            "id": row.id,
            "menuKey": row.menu_key,
            "label": row.label,
            "path": row.path,
            "componentKey": row.component_key,
            "parentId": row.parent_id,
            "level": 1 if row.parent_id is None else 2,
            "sort": row.sort,
            "isEnabled": row.is_enabled,
            "allowedUserIds": list(row.allowed_users.values_list("id", flat=True)),
        },
        status=201,
    )


@csrf_exempt
@superuser_api
@require_http_methods(["PATCH", "DELETE", "OPTIONS"])
def managed_menu_detail(request, pk: int):
    """
    PATCH /api/navigation/managed-menus/<pk>
    DELETE /api/navigation/managed-menus/<pk>
    """
    if request.method == "OPTIONS":
        return JsonResponse({})

    config = _ensure_active_navigation_config()
    row = (
        ManagedMenu.objects.filter(id=pk, config=config)
        .select_related("parent")
        .first()
    )
    if not row:
        return _json_error("菜单不存在", 404)

    if request.method == "DELETE":
        row.delete()
        return JsonResponse({"id": pk, "deleted": True})

    body = parse_json_body(request)
    if "menu_key" in body:
        menu_key = (body.get("menu_key") or "").strip()
        if not menu_key:
            return _json_error("menu_key 不能为空", 400)
        exists = ManagedMenu.objects.filter(
            config=config, menu_key=menu_key
        ).exclude(id=row.id)
        if exists.exists():
            return _json_error("menu_key 已存在", 409)
        row.menu_key = menu_key

    if "label" in body:
        label = (body.get("label") or "").strip()
        if not label:
            return _json_error("label 不能为空", 400)
        row.label = label

    if "path" in body:
        row.path = (body.get("path") or "").strip()
    if "component_key" in body:
        row.component_key = (body.get("component_key") or "").strip()
    if "sort" in body:
        sort = _parse_optional_int(body.get("sort"))
        if sort is None:
            return _json_error("sort 需为整数", 400)
        row.sort = sort
    if "is_enabled" in body:
        row.is_enabled = bool(body.get("is_enabled"))
    if "parent_id" in body:
        parent, parent_err = _validate_parent_menu(config, body.get("parent_id"))
        if parent_err:
            return parent_err
        if parent and parent.id == row.id:
            return _json_error("菜单不能把自己设为父级", 400)
        if parent and row.children.exists():
            return _json_error("当前菜单已有二级子菜单，不能再调整为二级菜单", 400)
        row.parent = parent

    row.save()
    if "allowed_user_ids" in body:
        uids = _normalize_user_ids(body.get("allowed_user_ids"))
        if uids is None:
            return _json_error("allowed_user_ids 须为整数数组", 400)
        users = list(get_user_model().objects.filter(id__in=uids))
        row.allowed_users.set(users)

    return JsonResponse(
        {
            "id": row.id,
            "menuKey": row.menu_key,
            "label": row.label,
            "path": row.path,
            "componentKey": row.component_key,
            "parentId": row.parent_id,
            "level": 1 if row.parent_id is None else 2,
            "sort": row.sort,
            "isEnabled": row.is_enabled,
            "allowedUserIds": list(row.allowed_users.values_list("id", flat=True)),
        }
    )


@csrf_exempt
@staff_api
@require_GET
def navigation_extra_routes_admin(request):
    """GET /api/navigation/extra-routes — 当前启用配置下的全部动态路由及组权限。"""
    config = _active_navigation_config()
    if not config:
        return JsonResponse({"items": [], "configVersion": None})

    items = []
    for r in config.extra_routes.all().order_by("sort", "id"):
        items.append(
            {
                "id": r.id,
                "routeId": r.route_id,
                "path": r.path,
                "componentKey": r.component_key,
                "isEnabled": r.is_enabled,
                "allowedGroupIds": list(
                    r.allowed_groups.values_list("id", flat=True)
                ),
            }
        )
    return JsonResponse({"configVersion": config.version, "items": items})


@csrf_exempt
@staff_api
@require_http_methods(["PATCH", "OPTIONS"])
def navigation_extra_route_patch(request, pk: int):
    """PATCH /api/navigation/extra-routes/<pk> — 设置 allowed_group_ids。"""
    if request.method == "OPTIONS":
        return JsonResponse({})

    config = _active_navigation_config()
    if not config:
        return _json_error("没有启用的导航配置", 404)

    row = ExtraRoute.objects.filter(id=pk, config=config).first()
    if not row:
        return _json_error("路由记录不存在", 404)

    body = parse_json_body(request)
    if "allowed_group_ids" not in body:
        return _json_error("缺少 allowed_group_ids", 400)
    gids = _normalize_group_ids(body.get("allowed_group_ids"))
    if gids is None:
        return _json_error("allowed_group_ids 须为整数数组", 400)

    groups = list(Group.objects.filter(id__in=gids))
    row.allowed_groups.set(groups)
    return JsonResponse(
        {
            "id": row.id,
            "routeId": row.route_id,
            "allowedGroupIds": list(row.allowed_groups.values_list("id", flat=True)),
        }
    )


@csrf_exempt
@staff_api
@require_GET
def navigation_menu_extra_admin(request):
    """GET /api/navigation/menu-extra-items — 追加菜单项及组权限。"""
    config = _active_navigation_config()
    if not config:
        return JsonResponse({"items": [], "configVersion": None})

    items = []
    for m in config.menu_extra_items.all().order_by("sort", "id"):
        items.append(
            {
                "id": m.id,
                "key": m.key,
                "label": m.label,
                "isEnabled": m.is_enabled,
                "allowedGroupIds": list(
                    m.allowed_groups.values_list("id", flat=True)
                ),
            }
        )
    return JsonResponse({"configVersion": config.version, "items": items})


@csrf_exempt
@staff_api
@require_http_methods(["PATCH", "OPTIONS"])
def navigation_menu_extra_patch(request, pk: int):
    """PATCH /api/navigation/menu-extra-items/<pk> — 设置 allowed_group_ids。"""
    if request.method == "OPTIONS":
        return JsonResponse({})

    config = _active_navigation_config()
    if not config:
        return _json_error("没有启用的导航配置", 404)

    row = MenuExtraItem.objects.filter(id=pk, config=config).first()
    if not row:
        return _json_error("菜单项不存在", 404)

    body = parse_json_body(request)
    if "allowed_group_ids" not in body:
        return _json_error("缺少 allowed_group_ids", 400)
    gids = _normalize_group_ids(body.get("allowed_group_ids"))
    if gids is None:
        return _json_error("allowed_group_ids 须为整数数组", 400)

    groups = list(Group.objects.filter(id__in=gids))
    row.allowed_groups.set(groups)
    return JsonResponse(
        {
            "id": row.id,
            "key": row.key,
            "allowedGroupIds": list(row.allowed_groups.values_list("id", flat=True)),
        }
    )
