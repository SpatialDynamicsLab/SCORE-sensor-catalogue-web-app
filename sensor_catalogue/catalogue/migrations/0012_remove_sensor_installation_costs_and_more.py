# Generated by Django 4.1.6 on 2023-03-29 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_sensor_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='installation_costs',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='installation_operation',
        ),
        migrations.AddField(
            model_name='sensor',
            name='assembly_operation_public_involvement',
            field=models.CharField(blank=True, max_length=300, verbose_name='Public Involvement & Assembly Operations'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='data_analysis_public_involvement',
            field=models.CharField(blank=True, max_length=300, verbose_name='Public Involvement & Data Analysis Operations'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='deployment_costs',
            field=models.CharField(blank=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default=None, max_length=1, null=True, verbose_name='Deployment Cost'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='deployment_operation',
            field=models.ForeignKey(blank=True, default=None, max_length=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.installationoperation', verbose_name='Deployment operation Complexity'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='deployment_operation_public_involvement',
            field=models.CharField(blank=True, max_length=300, verbose_name='Public Involvement & Deployment Operations'),
        ),
    ]