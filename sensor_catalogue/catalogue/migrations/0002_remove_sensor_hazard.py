# Generated by Django 4.1.6 on 2023-02-27 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sensor",
            name="hazard",
        ),
    ]
