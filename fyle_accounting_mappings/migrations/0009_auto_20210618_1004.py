# Generated by Django 3.0.3 on 2021-06-18 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_accounting_mappings', '0008_auto_20210604_0713'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mappingsetting',
            unique_together={('source_field', 'destination_field', 'workspace')},
        ),
    ]
