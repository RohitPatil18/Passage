# Generated by Django 4.1.3 on 2023-03-07 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                (
                    "name",
                    models.CharField(max_length=150, unique=True, verbose_name="name"),
                ),
                (
                    "permissions",
                    models.ManyToManyField(
                        blank=True, to="auth.permission", verbose_name="permissions"
                    ),
                ),
            ],
            options={
                "db_table": "auth_role",
            },
        ),
    ]
