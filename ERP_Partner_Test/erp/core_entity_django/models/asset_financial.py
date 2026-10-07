from decimal import Decimal

from django.db import models


class AssetFinancialInfo(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="financial_info",
    )

    acquisition_date = models.DateField(
        null=True,
        blank=True,
    )

    invoice_date = models.DateField(
        null=True,
        blank=True,
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
    )

    purchase_order_number = models.CharField(
        max_length=100,
        blank=True,
    )

    purchase_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    other_directly_attributable_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_capitalizable_cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.CharField(
        max_length=10,
    )

    exchange_rate = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        null=True,
        blank=True,
    )

    functional_currency_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )

    capitalization_date = models.DateField(
        null=True,
        blank=True,
    )

    # Future GL Account Service references
    gl_asset_account_id = models.UUIDField(
        null=True,
        blank=True,
    )

    accumulated_depreciation_account_id = models.UUIDField(
        null=True,
        blank=True,
    )

    depreciation_expense_account_id = models.UUIDField(
        null=True,
        blank=True,
    )

    cost_center_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    funding_source = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "far_asset_financial_info"