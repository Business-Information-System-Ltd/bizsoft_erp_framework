from django.db import models
from django.conf import settings
from core_entity_django.constants.constants import SourceType, LifecycleStatus, ValidationStatus, ApprovalStatus

class AssetCore(models.Model):
    draft_asset_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    asset_code = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    draft_date = models.DateField()

    entry_source = models.CharField(
        max_length=30,
        choices=SourceType.choices,
        default=SourceType.MANUAL,
    )

    lifecycle_status = models.CharField(
        max_length=30,
        choices=LifecycleStatus.choices,
        default=LifecycleStatus.DRAFT,
    )

    validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.INCOMPLETE,
    )

    capitalization_eligible = models.BooleanField(
        default=False
    )

    approval_status = models.CharField(
        max_length=30,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.NOT_SUBMITTED,
    )

    remarks = models.TextField(
        blank=True,
    )

    is_deleted = models.BooleanField(
        default=False
    )

    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_assets_prepared",
    )

    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_assets_updated",
    )

    last_updated_date = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "far_asset_core"
        ordering = ["-draft_date", "-id"]

        permissions = [
            (
                "view_far_assets",
                "Can view FAR draft assets",
            ),
            (
                "create_far_assets",
                "Can create FAR draft assets",
            ),
            (
                "update_far_assets",
                "Can update FAR draft assets",
            ),
            (
                "delete_far_assets",
                "Can delete FAR draft assets",
            ),
            (
                "validate_far_assets",
                "Can validate FAR draft assets",
            ),
            (
                "print_far_assets",
                "Can print FAR approval documents",
            ),
            (
                "capitalize_far_assets",
                "Can capitalize FAR assets",
            ),
            (
                "bulk_capitalize_far_assets",
                "Can bulk capitalize FAR assets",
            ),
        ]

        indexes = [
            models.Index(
                fields=["lifecycle_status"],
                name="idx_far_asset_status",
            ),
            models.Index(
                fields=["validation_status"],
                name="idx_far_asset_validation",
            ),
            models.Index(
                fields=["entry_source"],
                name="idx_far_asset_source",
            ),
            models.Index(
                fields=["capitalization_eligible"],
                name="idx_far_asset_eligible",
            ),
            models.Index(
                fields=["is_deleted"],
                name="idx_far_asset_deleted",
            ),
        ]

    def __str__(self):
        return self.draft_asset_number