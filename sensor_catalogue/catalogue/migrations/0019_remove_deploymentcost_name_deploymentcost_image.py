# Generated by Django 4.1.6 on 2023-04-22 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0018_remove_deploymentcost_image_deploymentcost_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deploymentcost',
            name='name',
        ),
        migrations.AddField(
            model_name='deploymentcost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='deployment_cost/%Y/%m/%d'),
        ),
    ]
