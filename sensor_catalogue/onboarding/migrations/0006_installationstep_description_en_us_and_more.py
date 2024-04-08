# Generated by Django 4.1.6 on 2024-04-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0005_installationstep_input_processing_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='installationstep',
            name='description_en_us',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='description_it',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='description_pt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='title_en_us',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='title_es',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='title_it',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='installationstep',
            name='title_pt',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('SCK-AQ-DUB', 'Smart Citizen Kit Air Quality - Dublin CCLL'), ('WU-PWS-DUB', 'Weather Station with 7-in-1 Sensor - Dublin CCLL'), ('WU-PWS', 'BRESSER WIFI ClearView Weather Station with 7-in-1 Sensor')], max_length=10),
        ),
    ]
