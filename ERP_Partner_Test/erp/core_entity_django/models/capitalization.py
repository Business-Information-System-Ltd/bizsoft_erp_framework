from django.conf import settings
from django.db import models


class CapitalizationTransaction(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.PROTECT,
        related_name="capitalization_transaction",
    )

    capitalization_date = models.DateField()

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
    )

    gl_asset_account = models.CharField(
        max_length=100,
    )

    transaction_reference = models.CharField(
        max_length=100,
        unique=True,
    )

    capitalized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="far_capitalizations",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "far_capitalization_transaction"

        ordering = [
            "-created_at"
        ]

        indexes = [
            models.Index(
                fields=["capitalization_date"],
                name="idx_far_cap_date",
            ),
        ]