# Generated by Django 4.1.6 on 2023-03-08 20:07

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hazard",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default=None,
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
    ]
