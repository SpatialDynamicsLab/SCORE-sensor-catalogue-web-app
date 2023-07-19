# Generated by Django 4.1.6 on 2023-07-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0021_sensorfaq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensorfaq',
            options={'verbose_name': 'FAQ', 'verbose_name_plural': "FAQ's"},
        ),
        migrations.AddField(
            model_name='sensor',
            name='relevant_to_ewss',
            field=models.BooleanField(default=True, verbose_name='Relevant to the EWSS'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='relevant_to_models',
            field=models.BooleanField(default=True, verbose_name='Relevant to WP3 Models'),
        ),
    ]
