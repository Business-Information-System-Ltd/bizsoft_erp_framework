from django.db import models


class AssetWipReference(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="wip_reference",
    )

    wip_item_reference = models.CharField(
        max_length=150,
    )

    wip_project_reference = models.CharField(
        max_length=150,
        blank=True,
    )

    allocated_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    source_balance_before = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )

    source_balance_after = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )

    transfer_date = models.DateField()

    approved = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "far_asset_wip_reference"

        indexes = [
            models.Index(
                fields=["wip_item_reference"],
                name="idx_far_wip_item",
            ),
            models.Index(
                fields=["wip_project_reference"],
                name="idx_far_wip_project",
            ),
        ]