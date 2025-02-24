from django.db import models


class FailedEvent(models.Model):
    """
    Model to store the failed events
    """
    id = models.AutoField(primary_key=True)
    routing_key = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_traceback = models.TextField(null=True)
    workspace_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'failed_events'
        app_label = 'fyle_accounting_library.rabbitmq'
