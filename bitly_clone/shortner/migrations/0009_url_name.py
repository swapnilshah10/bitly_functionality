# Generated by Django 4.1.7 on 2024-11-04 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortner", "0008_url_ip2"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="name",
            field=models.CharField(max_length=200, null=True),
        ),
    ]