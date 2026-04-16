from django.core.management.base import BaseCommand
from django.db import transaction

from apps.user.models import ExtraRoute, MenuExtraItem, MenuPatch, NavigationConfig


DEFAULT_MENU_PATCHES = [
    {"match_key": "/dashboard", "label": "首页（后端下发）", "sort": 10},
]

DEFAULT_MENU_EXTRA_ITEMS = [
    {"key": "/integration/backend-demo", "label": "后端下发菜单", "sort": 10},
]

DEFAULT_EXTRA_ROUTES = [
    {
        "route_id": "integration-backend-demo",
        "path": "integration/backend-demo",
        "component_key": "placeholder",
        "sort": 10,
    },
]


class Command(BaseCommand):
    help = "初始化路由菜单配置数据（NavigationConfig / MenuPatch / MenuExtraItem / ExtraRoute）"

    def add_arguments(self, parser):
        parser.add_argument(
            "--nav-version",
            default="server-1",
            help="初始化后的版本号，默认 server-1",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="先清空所有导航配置，再写入默认数据",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        version = options["nav_version"]
        should_reset = options["reset"]

        if should_reset:
            NavigationConfig.objects.all().delete()
            self.stdout.write(self.style.WARNING("已清空历史导航配置数据"))

        config, created = NavigationConfig.objects.get_or_create(
            version=version,
            defaults={"is_active": True},
        )

        if not config.is_active:
            config.is_active = True
            config.save(update_fields=["is_active", "updated_at"])

        # 只保留当前版本为 active，避免接口返回歧义
        NavigationConfig.objects.exclude(id=config.id).update(is_active=False)

        patch_count = self._seed_menu_patches(config)
        extra_item_count = self._seed_menu_extra_items(config)
        extra_route_count = self._seed_extra_routes(config)

        action = "创建" if created else "更新"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action}配置完成 version={config.version} | "
                f"menu_patches={patch_count}, "
                f"menu_extra_items={extra_item_count}, "
                f"extra_routes={extra_route_count}"
            )
        )

    def _seed_menu_patches(self, config):
        count = 0
        for row in DEFAULT_MENU_PATCHES:
            MenuPatch.objects.update_or_create(
                config=config,
                match_key=row["match_key"],
                defaults={
                    "label": row["label"],
                    "sort": row["sort"],
                    "is_enabled": True,
                },
            )
            count += 1
        return count

    def _seed_menu_extra_items(self, config):
        count = 0
        for row in DEFAULT_MENU_EXTRA_ITEMS:
            MenuExtraItem.objects.update_or_create(
                config=config,
                key=row["key"],
                defaults={
                    "label": row["label"],
                    "sort": row["sort"],
                    "is_enabled": True,
                },
            )
            count += 1
        return count

    def _seed_extra_routes(self, config):
        count = 0
        for row in DEFAULT_EXTRA_ROUTES:
            ExtraRoute.objects.update_or_create(
                route_id=row["route_id"],
                defaults={
                    "config": config,
                    "path": row["path"],
                    "component_key": row["component_key"],
                    "sort": row["sort"],
                    "is_enabled": True,
                },
            )
            count += 1
        return count
