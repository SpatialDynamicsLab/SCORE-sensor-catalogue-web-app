# Generated by Django 4.1.6 on 2023-04-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_remove_sensor_installation_costs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assemblyoperation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='difficulty/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='citizenscienceoperation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='difficulty/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='dataanalysisoperation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='difficulty/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='deploymentoperation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='difficulty/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='purchaseoperation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='difficulty/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='wifi_connection',
            field=models.BooleanField(default=True, verbose_name='Wi-Fi Connection'),
        ),
    ]
