from django.conf import settings
from django.db import models
from core_entity_django.constants.constants import StatusType


class AssetImportBatch(models.Model):



    batch_number = models.CharField(
        max_length=50,
        unique=True,
    )

    file_name = models.CharField(
        max_length=255,
    )

    file_type = models.CharField(
        max_length=20,
    )

    template_version = models.CharField(
        max_length=50,
    )

    status = models.CharField(
        max_length=20,
        choices=StatusType.CHOICES,
        default=StatusType.UPLOADED,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_import_batches",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    total_rows = models.PositiveIntegerField(
        default=0,
    )

    valid_rows = models.PositiveIntegerField(
        default=0,
    )

    error_rows = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "far_asset_import_batch"
        ordering = ["-uploaded_at"]