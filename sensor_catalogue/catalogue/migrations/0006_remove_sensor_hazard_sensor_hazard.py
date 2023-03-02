# Generated by Django 4.1.6 on 2023-02-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0005_alter_sensor_id_old"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sensor",
            name="hazard",
        ),
        migrations.AddField(
            model_name="sensor",
            name="hazard",
            field=models.ManyToManyField(
                blank=True, to="catalogue.hazard", verbose_name="Hazard"
            ),
        ),
    ]
