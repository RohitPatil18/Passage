from django.db import migrations

from authmod.models import RoleChoice


def create_default_roles(apps, schema_editor):
    Role = apps.get_model("authmod", "Role")

    for role in RoleChoice.choices:
        Role.objects.create(id=role[0], name=role[1])


class Migration(migrations.Migration):
    dependencies = [
        ("authmod", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_default_roles)]
