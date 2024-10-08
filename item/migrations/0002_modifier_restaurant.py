# Generated by Django 5.1.1 on 2024-09-08 01:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_user", "0001_initial"),
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="modifier",
            name="restaurant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="modifiers",
                to="app_user.restaurant",
            ),
        ),
    ]
