# Generated by Django 4.1.6 on 2023-03-29 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_alter_sensor_accuracy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='short_description',
            field=models.TextField(blank=True, verbose_name='Short Description'),
        ),
    ]