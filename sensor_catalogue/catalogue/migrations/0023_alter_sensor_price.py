# Generated by Django 4.1.6 on 2023-09-07 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0022_alter_sensorfaq_options_sensor_relevant_to_ewss_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cost(€)'),
        ),
    ]
