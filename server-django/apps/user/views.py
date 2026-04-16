from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .auth_support import resolve_target_user
from .models import NavigationConfig


@require_GET
def navigation_manifest(request):
    """
    提供前端动态路由/菜单配置。
    数据来源：NavigationConfig + 子表（MenuPatch / MenuExtraItem / ExtraRoute / ManagedMenu）。
    """
    config = (
        NavigationConfig.objects.prefetch_related(
            "menu_patches",
            "menu_extra_items__allowed_groups",
            "extra_routes__allowed_groups",
            "managed_menus__allowed_users",
            "managed_menus__parent",
        )
        .filter(is_active=True)
        .first()
    )

    if not config:
        data = {
            "version": "server-empty",
            "items": [],
        }
        return JsonResponse(data)

    target_user = resolve_target_user(request)
    is_superuser = bool(target_user and target_user.is_superuser)
    user_group_ids = set(target_user.groups.values_list("id", flat=True)) if target_user else set()
    target_user_id = target_user.id if target_user else None

    # 统一结构：不同能力（补丁菜单 / 新增菜单 / 新增路由）统一为 items[]，
    # 通过 type 区分具体语义，避免前端处理三套不同对象结构。
    items = []
    for item in config.menu_patches.filter(is_enabled=True):
        items.append(
            {
                "id": f"menu_patch:{item.id}",
                "type": "menu_patch",
                "matchKey": item.match_key,
                "key": None,
                "label": item.label,
                "path": None,
                "componentKey": None,
            }
        )

    for item in config.menu_extra_items.filter(is_enabled=True):
        allowed_group_ids = {
            group.id for group in item.allowed_groups.all()
        }
        is_public = not allowed_group_ids
        has_access = is_superuser or is_public or bool(
            user_group_ids & allowed_group_ids
        )
        if has_access:
            items.append(
                {
                    "id": f"menu_extra:{item.id}",
                    "type": "menu_extra",
                    "matchKey": None,
                    "key": item.key,
                    "label": item.label,
                    "path": None,
                    "componentKey": None,
                }
            )

    for item in config.extra_routes.filter(is_enabled=True):
        allowed_group_ids = {
            group.id for group in item.allowed_groups.all()
        }
        is_public = not allowed_group_ids
        has_access = is_superuser or is_public or bool(
            user_group_ids & allowed_group_ids
        )
        if has_access:
            items.append(
                {
                    "id": item.route_id,
                    "type": "extra_route",
                    "matchKey": None,
                    "key": None,
                    "label": None,
                    "path": item.path,
                    "componentKey": item.component_key,
                }
            )

    enabled_managed_menus = config.managed_menus.filter(is_enabled=True).order_by("sort", "id")
    managed_menu_enabled = enabled_managed_menus.exists()
    for item in enabled_managed_menus:
        allowed_user_ids = set(item.allowed_users.values_list("id", flat=True))
        # 用户菜单权限采用“显式授权”：
        # - 超级管理员：可见全部
        # - 其他用户：仅可见被分配给自己的菜单
        has_access = is_superuser or bool(
            target_user_id and target_user_id in allowed_user_ids
        )
        if has_access:
            items.append(
                {
                    "id": f"managed_menu:{item.id}",
                    "type": "managed_menu",
                    "matchKey": None,
                    "key": item.menu_key,
                    "label": item.label,
                    "path": item.path or None,
                    "componentKey": item.component_key or None,
                    "parentKey": item.parent.menu_key if item.parent else None,
                    "sort": item.sort,
                }
            )

    data = {
        "version": config.version,
        # 供前端判断是否进入“受控菜单模式”（非超管仅显示被授权菜单）
        "managedMenuEnabled": managed_menu_enabled,
        "items": items,
    }
    return JsonResponse(data)
