# Generated by Django 4.2.18 on 2025-02-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabbitmq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failedevent',
            name='error_traceback',
            field=models.TextField(null=True),
        ),
    ]
