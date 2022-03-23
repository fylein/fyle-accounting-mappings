# Generated by Django 3.1.14 on 2022-03-23 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0026_auto_20220323_0914'),
        ('fyle_accounting_mappings', '0012_auto_20211206_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappingsetting',
            name='workspace',
            field=models.ForeignKey(help_text='Reference to Workspace model', on_delete=django.db.models.deletion.PROTECT, related_name='mapping_settings', to='workspaces.workspace'),
        )
    ]
