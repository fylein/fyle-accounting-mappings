# Generated by Django 4.2.18 on 2025-02-26 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabbitmq', '0002_alter_failedevent_error_traceback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failedevent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when the failed event was created'),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='error_traceback',
            field=models.TextField(help_text='Error traceback from the failed event', null=True),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='id',
            field=models.AutoField(help_text='Primary key for the failed event', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='payload',
            field=models.JSONField(default=dict, help_text='JSON payload of the failed event'),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='routing_key',
            field=models.CharField(help_text='RabbitMQ routing key for the failed event', max_length=255),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp when the failed event was last updated'),
        ),
        migrations.AlterField(
            model_name='failedevent',
            name='workspace_id',
            field=models.IntegerField(help_text='Reference to the workspace where this event occurred', null=True),
        ),
    ]
