from django.db import models


class AssetSupplierAcquisition(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="supplier_info",
    )

    supplier_partner_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
    )

    procurement_method = models.CharField(
        max_length=100,
        blank=True,
    )

    contract_number = models.CharField(
        max_length=100,
        blank=True,
    )

    delivery_note_number = models.CharField(
        max_length=100,
        blank=True,
    )

    warranty_start_date = models.DateField(
        null=True,
        blank=True,
    )

    warranty_end_date = models.DateField(
        null=True,
        blank=True,
    )

    warranty_provider_partner_id = models.UUIDField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "far_asset_supplier_acquisition"

        indexes = [
            models.Index(
                fields=["supplier_partner_id"],
                name="idx_far_supplier_partner",
            ),
            models.Index(
                fields=["warranty_provider_partner_id"],
                name="idx_far_warranty_provider",
            ),
        ]