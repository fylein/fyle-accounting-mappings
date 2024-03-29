# Generated by Django 3.0.3 on 2021-06-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0007_auto_20210409_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappingsetting',
            name='expense_field_id',
            field=models.IntegerField(help_text='Expense Field ID', null=True, unique=True),
        ),
        migrations.AddField(
            model_name='mappingsetting',
            name='import_to_fyle',
            field=models.BooleanField(default=False, help_text='Import to Fyle or not'),
        ),
        migrations.AddField(
            model_name='mappingsetting',
            name='is_custom',
            field=models.BooleanField(default=False, help_text='Custom Field or not'),
        ),
        migrations.AlterField(
            model_name='mappingsetting',
            name='destination_field',
            field=models.CharField(default='DEFAULT', help_text='Destination mapping field', max_length=255),
            preserve_default=False,
        ),
    ]
