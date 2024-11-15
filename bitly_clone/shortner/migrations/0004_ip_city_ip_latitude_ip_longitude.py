# Generated by Django 4.1.7 on 2023-04-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortner", "0003_ip"),
    ]

    operations = [
        migrations.AddField(
            model_name="ip",
            name="city",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="ip",
            name="latitude",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="ip",
            name="longitude",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
