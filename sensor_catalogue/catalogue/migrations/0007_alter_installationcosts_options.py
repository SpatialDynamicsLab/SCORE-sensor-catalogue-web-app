# Generated by Django 4.1.6 on 2023-03-09 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0006_alter_sensor_purchase_operation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="installationcosts",
            options={
                "verbose_name": "Installation Cost",
                "verbose_name_plural": "Install Costs",
            },
        ),
    ]