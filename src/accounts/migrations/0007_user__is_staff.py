# Generated by Django 4.1.3 on 2023-03-07 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_user_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="_is_staff",
            field=models.BooleanField(
                db_column="is_staff",
                default=False,
                help_text="Designates whether the user can log into this admin site.",
                verbose_name="staff status",
            ),
        ),
    ]
