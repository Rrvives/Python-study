from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0004_managedmenu"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="managedmenu",
            name="allowed_groups",
        ),
        migrations.AddField(
            model_name="managedmenu",
            name="allowed_users",
            field=models.ManyToManyField(
                blank=True,
                help_text="留空表示所有用户可见；设置后仅这些用户可见。",
                related_name="navigation_managed_menus",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
