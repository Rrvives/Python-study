from django.contrib import admin

from .models import (
    ApiToken,
    ExtraRoute,
    ManagedMenu,
    MenuExtraItem,
    MenuPatch,
    NavigationConfig,
)


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "key_preview")
    search_fields = ("user__username", "key")
    readonly_fields = ("key", "created_at")

    @staticmethod
    def key_preview(obj: ApiToken) -> str:
        k = obj.key or ""
        return f"{k[:8]}…" if len(k) > 10 else k

    key_preview.short_description = "Token 预览"


class MenuPatchInline(admin.TabularInline):
    model = MenuPatch
    extra = 1


class MenuExtraItemInline(admin.TabularInline):
    model = MenuExtraItem
    extra = 1


class ExtraRouteInline(admin.TabularInline):
    model = ExtraRoute
    extra = 1


class ManagedMenuInline(admin.TabularInline):
    model = ManagedMenu
    extra = 1


@admin.register(NavigationConfig)
class NavigationConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("version",)
    inlines = [MenuPatchInline, MenuExtraItemInline, ExtraRouteInline, ManagedMenuInline]


@admin.register(MenuPatch)
class MenuPatchAdmin(admin.ModelAdmin):
    list_display = ("id", "match_key", "label", "sort", "is_enabled", "config")
    list_filter = ("is_enabled",)
    search_fields = ("match_key", "label")


@admin.register(MenuExtraItem)
class MenuExtraItemAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "label", "sort", "is_enabled", "config", "group_names")
    list_filter = ("is_enabled",)
    search_fields = ("key", "label")
    filter_horizontal = ("allowed_groups",)

    @staticmethod
    def group_names(obj):
        names = list(obj.allowed_groups.values_list("name", flat=True))
        return ", ".join(names) if names else "公开"

    group_names.short_description = "可见组"


@admin.register(ExtraRoute)
class ExtraRouteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "route_id",
        "path",
        "component_key",
        "sort",
        "is_enabled",
        "config",
        "group_names",
    )
    list_filter = ("is_enabled", "component_key")
    search_fields = ("route_id", "path", "component_key")
    filter_horizontal = ("allowed_groups",)

    @staticmethod
    def group_names(obj):
        names = list(obj.allowed_groups.values_list("name", flat=True))
        return ", ".join(names) if names else "公开"

    group_names.short_description = "可访问组"


@admin.register(ManagedMenu)
class ManagedMenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "menu_key",
        "label",
        "path",
        "parent",
        "sort",
        "is_enabled",
        "config",
        "user_names",
    )
    list_filter = ("is_enabled",)
    search_fields = ("menu_key", "label", "path")
    filter_horizontal = ("allowed_users",)

    @staticmethod
    def user_names(obj):
        names = list(obj.allowed_users.values_list("username", flat=True))
        return ", ".join(names) if names else "公开"

    user_names.short_description = "可见用户"
