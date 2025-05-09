# Generated by Django 4.1.6 on 2024-03-25 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0004_installationstep_input_label_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='installationstep',
            name='input_processing_url',
            field=models.URLField(blank=True, help_text='URL used for processing and input.', max_length=255, null=True),
        ),
    ]
