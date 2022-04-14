# Generated by Django 3.1.13 on 2021-12-06 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0011_categorymapping_employeemapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationattribute',
            name='detail',
            field=models.JSONField(help_text='Detailed destination attributes payload', null=True),
        ),
        migrations.AlterField(
            model_name='expenseattribute',
            name='detail',
            field=models.JSONField(help_text='Detailed expense attributes payload', null=True),
        ),
    ]