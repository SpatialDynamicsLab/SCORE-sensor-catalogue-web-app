# Generated by Django 4.1.6 on 2023-03-10 11:39

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0008_rename_installationcosts_installationcost"),
    ]

    operations = [
        migrations.AddField(
            model_name="assemblyoperation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="citizenscienceoperation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="dataanalysisoperation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="installationoperation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="purchaseoperation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
            ),
        ),
    ]