from django.db import models
from core_entity_django.constants.constants import ErrorType

class AssetImportError(models.Model):



    batch = models.ForeignKey(
        "core_entity_django.AssetImportBatch",
        on_delete=models.CASCADE,
        related_name="errors",
    )

    row_number = models.PositiveIntegerField()

    field_name = models.CharField(
        max_length=100,
        blank=True,
    )

    error_code = models.CharField(
        max_length=100,
    )

    error_message = models.TextField()

    error_type = models.CharField(
        max_length=20,
        choices=ErrorType.CHOICES,
        default=ErrorType.BLOCKING,
    )

    suggested_correction = models.TextField(
        blank=True,
    )

    corrected = models.BooleanField(
        default=False,
    )

    corrected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "far_asset_import_error"

        indexes = [
            models.Index(
                fields=["batch", "row_number"],
                name="idx_far_import_err_row",
            ),
        ]