# Generated by Django 4.1.6 on 2023-02-10 20:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalogue", "0005_rename_sensor_slug_sensor_slug"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OrderedSensor",
            new_name="OrderSensor",
        ),
    ]
