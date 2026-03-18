from django.db import models
from django.contrib.postgres.fields import ArrayField

from apps.workspaces.models import Workspace

from .helpers import generate_choices_from_enum
from .enums import DimensionDetailSourceTypeEnum


SOURCE_TYPE_CHOICES = generate_choices_from_enum(DimensionDetailSourceTypeEnum)


class DimensionDetail(models.Model):
    """
    Sage Intacct Dimension Details
    DB Table: dimension_details:
    """
    id = models.AutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT, help_text='Reference to Workspace')
    attribute_type = models.CharField(max_length=255, help_text='Attribute Type')
    display_name = models.CharField(max_length=255, help_text='Attribute Display Name')
    source_type = models.CharField(help_text='Source Type', null=False, default=DimensionDetailSourceTypeEnum.ACCOUNTING.value, max_length=100, choices=SOURCE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    class Meta:
        db_table = 'dimension_details'
        unique_together = ('attribute_type', 'display_name', 'workspace_id', 'source_type')

    @staticmethod
    def bulk_create_or_update_dimension_details(dimensions: list[dict], workspace_id: int, source_type: str) -> None:
        """
        Bulk create or update dimension details
        """
        attribute_types = set([dimension['attribute_type'] for dimension in dimensions])

        existing_dimensions = DimensionDetail.objects.filter(
            attribute_type__in=attribute_types,
            workspace_id=workspace_id,
            source_type=source_type
        ).values(
            'id',
            'attribute_type',
            'display_name',
            'source_type'
        )

        existing_dimension_map = {dimension['attribute_type']: dimension for dimension in existing_dimensions}

        dimensions_to_be_created = []
        dimensions_to_be_updated = []

        for dimension in dimensions:
            if dimension['attribute_type'] not in existing_dimension_map:
                dimensions_to_be_created.append(DimensionDetail(
                    attribute_type=dimension['attribute_type'],
                    display_name=dimension['display_name'],
                    source_type=dimension['source_type'],
                    workspace_id=workspace_id
                ))
            else:
                existing_dimension = existing_dimension_map[dimension['attribute_type']]
                if existing_dimension['display_name'] != dimension['display_name']:
                    dimensions_to_be_updated.append(DimensionDetail(
                        id=existing_dimension['id'],
                        attribute_type=dimension['attribute_type'],
                        display_name=dimension['display_name'],
                        source_type=dimension['source_type'],
                        workspace_id=workspace_id
                    ))

        if dimensions_to_be_created:
            DimensionDetail.objects.bulk_create(dimensions_to_be_created, batch_size=50)

        if dimensions_to_be_updated:
            DimensionDetail.objects.bulk_update(dimensions_to_be_updated, ['display_name'], batch_size=50)


class DataMigrationBatch(models.Model):
    """
    Data Migration Batch
    """
    id = models.AutoField(primary_key=True)
    object_ids = ArrayField(models.IntegerField(), help_text='Object IDs')
    procedure_name = models.TextField(null=False, help_text='Procedure Name')
    database_name = models.CharField(null=False, max_length=100, help_text='Database Name')
    max_attempts = models.IntegerField(default=3, help_text='Max Attempts')
    num_attempts = models.IntegerField(default=0, help_text='Number of Attempts')
    started_at = models.DateTimeField(null=True, help_text='Started At')
    completed_at = models.DateTimeField(null=True, help_text='Completed At')
    failed_at = models.DateTimeField(null=True, help_text='Failed At')
    error = models.JSONField(null=True, help_text='Error')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created At')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated At')

    class Meta:
        db_table = 'data_migration_batches'
        indexes = [
            models.Index(
                fields=['database_name', 'id'],
                name='idx_dmb_unprocessed',
                condition=models.Q(num_attempts=0, completed_at__isnull=True),
            ),
            models.Index(
                fields=['database_name', 'num_attempts', 'id'],
                name='idx_dmb_retry',
                condition=models.Q(completed_at__isnull=True, num_attempts__gt=0),
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(num_attempts__lte=models.F('max_attempts')),
                name='num_attempts_lte_max_attempts'
            ),
            models.CheckConstraint(
                check=models.Q(object_ids__len__lte=200),
                name='object_ids_len_lte_200'
            ),
        ]
