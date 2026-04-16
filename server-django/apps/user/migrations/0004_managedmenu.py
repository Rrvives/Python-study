from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_apitoken"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagedMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("menu_key", models.CharField(max_length=255)),
                ("label", models.CharField(max_length=255)),
                (
                    "path",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="可点击菜单建议以 / 开头（如 /system/menu-management）",
                        max_length=255,
                    ),
                ),
                (
                    "component_key",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="可选：若 path 对应动态组件，可填写 routeRegistry 里的 componentKey",
                        max_length=128,
                    ),
                ),
                ("sort", models.PositiveIntegerField(default=0)),
                ("is_enabled", models.BooleanField(default=True)),
                (
                    "config",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managed_menus",
                        to="user.navigationconfig",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="user.managedmenu",
                    ),
                ),
            ],
            options={
                "db_table": "user_managed_menu",
                "ordering": ["sort", "id"],
                "unique_together": {("config", "menu_key")},
            },
        ),
        migrations.AddField(
            model_name="managedmenu",
            name="allowed_groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="留空表示所有用户可见；设置后仅这些用户组可见。",
                related_name="navigation_managed_menus",
                to="auth.group",
            ),
        ),
    ]
