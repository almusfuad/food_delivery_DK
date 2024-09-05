# Generated by Django 5.1.1 on 2024-09-04 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0002_modifier_itemmodifier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemmodifier",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="modifiers",
                to="item.item",
            ),
        ),
        migrations.AlterField(
            model_name="itemmodifier",
            name="modifier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="item.modifier",
            ),
        ),
    ]
