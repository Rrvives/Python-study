from django.urls import path

from . import api_views
from .views import navigation_manifest

urlpatterns = [
    path("auth/login", api_views.auth_login, name="auth-login"),
    path("users", api_views.users_collection, name="users-collection"),
    path("users/<int:user_id>", api_views.users_patch, name="users-patch"),
    path(
        "users/<int:user_id>/menu-permissions",
        api_views.user_menu_permissions,
        name="users-menu-permissions",
    ),
    path("navigation/manifest", navigation_manifest, name="navigation-manifest"),
    path(
        "navigation/managed-menus",
        api_views.managed_menus_collection,
        name="navigation-managed-menus",
    ),
    path(
        "navigation/managed-menus/<int:pk>",
        api_views.managed_menu_detail,
        name="navigation-managed-menu-detail",
    ),
    path(
        "navigation/extra-routes",
        api_views.navigation_extra_routes_admin,
        name="navigation-extra-routes-admin",
    ),
    path(
        "navigation/extra-routes/<int:pk>",
        api_views.navigation_extra_route_patch,
        name="navigation-extra-route-patch",
    ),
    path(
        "navigation/menu-extra-items",
        api_views.navigation_menu_extra_admin,
        name="navigation-menu-extra-admin",
    ),
    path(
        "navigation/menu-extra-items/<int:pk>",
        api_views.navigation_menu_extra_patch,
        name="navigation-menu-extra-patch",
    ),
]
