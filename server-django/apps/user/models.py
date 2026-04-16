from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models


class ApiToken(models.Model):
    """
    简易 Bearer Token：登录成功后签发，供 SPA 放在 Authorization 头。
    同一用户再次登录会轮换新 token（见 auth_login 视图）。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="api_tokens",
    )
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_api_token"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"ApiToken(user={self.user_id})"


class NavigationConfig(models.Model):
    """
    导航配置主表。

    当前按单条启用配置使用（is_active=True 的最新一条）。
    后续可扩展 tenant_id / role_code 等维度。
    """

    version = models.CharField(max_length=64, default="server-1")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_navigation_config"
        ordering = ["-id"]

    def __str__(self):
        return f"NavigationConfig(version={self.version}, active={self.is_active})"


class MenuPatch(models.Model):
    """
    覆盖已有菜单项文案（match_key 与前端菜单 key 对齐）。
    """

    config = models.ForeignKey(
        NavigationConfig,
        on_delete=models.CASCADE,
        related_name="menu_patches",
    )
    match_key = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    sort = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "user_menu_patch"
        ordering = ["sort", "id"]

    def __str__(self):
        return f"MenuPatch({self.match_key} -> {self.label})"


class MenuExtraItem(models.Model):
    """
    追加到侧栏末尾的菜单项（key 为绝对路由路径）。
    """

    config = models.ForeignKey(
        NavigationConfig,
        on_delete=models.CASCADE,
        related_name="menu_extra_items",
    )
    key = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    allowed_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="navigation_menu_extra_items",
        help_text="留空表示所有用户可见；设置后仅这些用户组可见。",
    )
    sort = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "user_menu_extra_item"
        ordering = ["sort", "id"]

    def __str__(self):
        return f"MenuExtraItem({self.key})"


class ExtraRoute(models.Model):
    """
    动态追加路由（path 为相对根布局的子路径）。
    """

    config = models.ForeignKey(
        NavigationConfig,
        on_delete=models.CASCADE,
        related_name="extra_routes",
    )
    route_id = models.CharField(max_length=128, unique=True)
    path = models.CharField(max_length=255)
    component_key = models.CharField(max_length=128)
    allowed_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="navigation_extra_routes",
        help_text="留空表示所有用户可访问；设置后仅这些用户组可访问。",
    )
    sort = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "user_extra_route"
        ordering = ["sort", "id"]

    def __str__(self):
        return f"ExtraRoute({self.route_id})"


class ManagedMenu(models.Model):
    """
    可视化菜单配置（仅支持两级）：
    - 一级菜单：parent 为空
    - 二级菜单：parent 指向一级菜单
    """

    config = models.ForeignKey(
        NavigationConfig,
        on_delete=models.CASCADE,
        related_name="managed_menus",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    menu_key = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    path = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="可点击菜单建议以 / 开头（如 /system/menu-management）",
    )
    component_key = models.CharField(
        max_length=128,
        blank=True,
        default="",
        help_text="可选：若 path 对应动态组件，可填写 routeRegistry 里的 componentKey",
    )
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="navigation_managed_menus",
        help_text="留空表示所有用户可见；设置后仅这些用户可见。",
    )
    sort = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "user_managed_menu"
        ordering = ["sort", "id"]
        unique_together = [("config", "menu_key")]

    def __str__(self):
        return f"ManagedMenu({self.menu_key})"
