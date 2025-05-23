# Generated by Django 4.2.20 on 2025-04-21 11:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0028_auto_20241226_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseattributesdeletioncache',
            name='cost_center_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=[], size=None),
        ),
        migrations.AddField(
            model_name='expenseattributesdeletioncache',
            name='custom_field_list',
            field=models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='expenseattributesdeletioncache',
            name='merchant_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=[], size=None),
        ),
    ]
