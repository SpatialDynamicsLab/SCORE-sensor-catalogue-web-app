# Generated by Django 4.1.6 on 2023-03-09 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0005_alter_sensor_assembly_operation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensor",
            name="purchase_operation",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalogue.purchaseoperation",
                verbose_name="Purchase Operation",
            ),
        ),
    ]