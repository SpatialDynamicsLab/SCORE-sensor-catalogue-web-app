# Generated by Django 4.1.6 on 2023-04-22 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_rename_installationcost_deploymentcost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='installation_costs',
        ),
        migrations.AddField(
            model_name='sensor',
            name='deployment_costs',
            field=models.CharField(blank=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default=None, max_length=1, null=True, verbose_name='Deployment Cost'),
        ),
    ]