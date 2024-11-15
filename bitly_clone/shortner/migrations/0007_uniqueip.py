# Generated by Django 4.1.7 on 2023-10-24 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortner", "0006_rename_created_at_ip_time_ip_method_ip_page"),
    ]

    operations = [
        migrations.CreateModel(
            name="UniqueIp",
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
                ("ip", models.CharField(default="", max_length=100, unique=True)),
            ],
        ),
    ]
