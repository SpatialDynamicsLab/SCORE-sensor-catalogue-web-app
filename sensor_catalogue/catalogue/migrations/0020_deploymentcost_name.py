# Generated by Django 4.1.6 on 2023-04-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0019_remove_deploymentcost_name_deploymentcost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploymentcost',
            name='name',
            field=models.CharField(blank=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], max_length=1),
        ),
    ]
