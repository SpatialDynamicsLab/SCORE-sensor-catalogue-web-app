# Generated by Django 4.1.6 on 2024-04-16 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0026_alter_sensor_project_year'),
        ('onboarding', '0008_alter_sensorthing_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorthing',
            name='location',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sensorthing',
            name='properties',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sensorthing',
            name='sensor',
            field=models.ForeignKey(default=18, on_delete=django.db.models.deletion.SET_DEFAULT, to='catalogue.sensor'),
        ),
    ]
