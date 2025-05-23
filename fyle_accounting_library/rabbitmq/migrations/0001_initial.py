# Generated by Django 4.2.18 on 2025-02-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workspaces','0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('routing_key', models.CharField(max_length=255)),
                ('payload', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('error_traceback', models.JSONField(default=dict)),
                ('workspace_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'failed_events',
            },
        ),
    ]
