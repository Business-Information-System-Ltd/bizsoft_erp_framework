from django.conf import settings
from django.db import models
from core_entity_django.constants.constants import ActionType

class AssetAuditLog(models.Model):


    asset = models.ForeignKey(
        "core_entity_django.AssetCore",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )

    action_type = models.CharField(
        max_length=30,
        choices=ActionType.CHOICES,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_audit_logs",
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    old_value = models.JSONField(
        null=True,
        blank=True,
    )

    new_value = models.JSONField(
        null=True,
        blank=True,
    )

    reason = models.TextField(
        blank=True,
    )

    source_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    device = models.CharField(
        max_length=255,
        blank=True,
    )

    batch_number = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "far_asset_audit_log"

        ordering = [
            "-timestamp"
        ]

        indexes = [
            models.Index(
                fields=[
                    "asset",
                    "timestamp",
                ],
                name="idx_far_audit_asset_time",
            ),
            models.Index(
                fields=[
                    "action_type",
                    "timestamp",
                ],
                name="idx_far_audit_action_time",
            ),
            models.Index(
                fields=[
                    "batch_number",
                ],
                name="idx_far_audit_batch",
            ),
        ]