# Generated by Django 4.1.6 on 2023-03-09 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0007_alter_installationcosts_options"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="InstallationCosts",
            new_name="InstallationCost",
        ),
    ]
