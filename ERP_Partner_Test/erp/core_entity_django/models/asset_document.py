from django.conf import settings
from django.db import models
from core_entity_django.constants.constants import DocumentType


class AssetDocument(models.Model):


    asset = models.ForeignKey(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.CHOICES,
    )

    file = models.FileField(
        upload_to="far/assets/%Y/%m/",
    )

    reference_number = models.CharField(
        max_length=150,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_documents_uploaded",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "far_asset_document"

        indexes = [
            models.Index(
                fields=["asset", "document_type"],
                name="idx_far_doc_asset_type",
            ),
        ]