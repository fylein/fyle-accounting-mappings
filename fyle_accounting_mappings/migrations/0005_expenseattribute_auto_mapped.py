# Generated by Django 3.0.3 on 2021-02-11 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0004_auto_20210127_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseattribute',
            name='auto_mapped',
            field=models.BooleanField(default=False, help_text='Indicates whether the field is auto mapped or not'),
        ),
    ]