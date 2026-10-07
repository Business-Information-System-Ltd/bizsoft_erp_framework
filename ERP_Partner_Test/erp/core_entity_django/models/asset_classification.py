from django.db import models


class AssetClassification(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="classification",
    )

    asset_class = models.CharField(
        max_length=150,
    )

    asset_category = models.CharField(
        max_length=150,
    )

    asset_subcategory = models.CharField(
        max_length=150,
        blank=True,
    )

    asset_group = models.CharField(
        max_length=150,
        blank=True,
    )

    depreciation_policy_group = models.CharField(
        max_length=150,
        blank=True,
    )

    useful_life = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    residual_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    depreciation_method = models.CharField(
        max_length=100,
        blank=True,
    )

    capitalization_threshold_check = models.BooleanField(
        default=False,
    )

    tax_asset_category = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "far_asset_classification"

        indexes = [
            models.Index(
                fields=["asset_class"],
                name="idx_far_class_class",
            ),
            models.Index(
                fields=["asset_category"],
                name="idx_far_class_category",
            ),
        ]