# Generated by Django 4.1.6 on 2023-02-09 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0003_alter_sensor_minimum_purchase_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensor",
            name="data_refresh_time",
            field=models.IntegerField(
                blank=True,
                default=5,
                null=True,
                verbose_name="Data Refresh Duration (Minutes)",
            ),
        ),
    ]
