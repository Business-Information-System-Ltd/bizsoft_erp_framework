from django.db import models


class AssetBasicInfo(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="basic_info",
    )

    asset_name = models.CharField(max_length=255)

    asset_description = models.TextField(blank=True)

    brand = models.CharField(
        max_length=150,
        blank=True,
    )

    model = models.CharField(
        max_length=150,
        blank=True,
    )

    serial_number = models.CharField(
        max_length=150,
        blank=True,
    )

    manufacturer = models.CharField(
        max_length=150,
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=4,
    )

    unit_of_measure = models.CharField(
        max_length=50,
    )

    asset_type = models.CharField(
        max_length=100,
    )

    parent_asset = models.ForeignKey(
        "core_entity_django.AssetCore",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="component_assets",
    )

    component_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "far_asset_basic_info"

        indexes = [
            models.Index(
                fields=["asset_name"],
                name="idx_far_basic_name",
            ),
            models.Index(
                fields=["serial_number"],
                name="idx_far_basic_serial",
            ),
            models.Index(
                fields=["asset_type"],
                name="idx_far_basic_type",
            ),
        ]

    def __str__(self):
        return self.asset_name