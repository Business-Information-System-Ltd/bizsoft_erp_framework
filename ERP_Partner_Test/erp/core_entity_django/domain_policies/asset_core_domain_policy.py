from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from core_entity_django.models import (
    AssetCore,
    AssetDocument,
)


def validate_draft_editable(asset):
    if asset.is_deleted:
        raise ValidationError(
            "Deleted assets cannot be edited."
        )

    if asset.lifecycle_status != AssetCore.LifecycleStatus.DRAFT:
        raise ValidationError(
            "Only Draft assets can be edited."
        )

    if asset.approval_status == AssetCore.ApprovalStatus.APPROVED:
        raise ValidationError(
            "Approved assets cannot be edited."
        )


def validate_draft_deletable(asset):
    if asset.is_deleted:
        raise ValidationError(
            "Asset is already deleted."
        )

    if asset.lifecycle_status != AssetCore.LifecycleStatus.DRAFT:
        raise ValidationError(
            "Only Draft assets can be deleted."
        )

    if asset.approval_status in (
        AssetCore.ApprovalStatus.PRINTED,
        AssetCore.ApprovalStatus.APPROVED,
    ):
        raise ValidationError(
            "Approval-locked assets cannot be deleted."
        )


def validate_positive_quantity(quantity):
    if quantity is None or quantity <= 0:
        raise ValidationError(
            "Quantity must be greater than zero."
        )


def validate_positive_cost(cost):
    if cost is None or cost <= 0:
        raise ValidationError(
            "Cost must be greater than zero."
        )


def validate_useful_life(useful_life):
    if useful_life is not None and useful_life <= 0:
        raise ValidationError(
            "Useful life must be greater than zero."
        )


def validate_warranty_dates(start_date, end_date):
    if start_date and end_date and end_date < start_date:
        raise ValidationError(
            "Warranty end date cannot be earlier than start date."
        )


def _require_depreciation_fields(asset):
    classification = asset.classification
    financial = asset.financial_info

    is_depreciable = bool(
        classification.depreciation_policy_group
        or classification.depreciation_method
    )

    if not is_depreciable:
        return

    if classification.useful_life is None:
        raise ValidationError(
            "Useful life is required for depreciable asset."
        )

    if not classification.depreciation_method:
        raise ValidationError(
            "Depreciation method is required for depreciable asset."
        )

    if not financial.accumulated_depreciation_account:
        raise ValidationError(
            "Accumulated depreciation account is required."
        )

    if not financial.depreciation_expense_account:
        raise ValidationError(
            "Depreciation expense account is required."
        )


def _validate_source_evidence(asset):
    require_invoice = getattr(
        settings,
        "FAR_REQUIRE_INVOICE_DOCUMENT_FOR_CAPITALIZATION",
        False,
    )

    require_approval_document = getattr(
        settings,
        "FAR_REQUIRE_APPROVAL_DOCUMENT",
        False,
    )

    if asset.entry_source == AssetCore.SourceType.WIP_TRANSFER:
        if not hasattr(asset, "wip_reference"):
            raise ValidationError(
                "WIP reference is required for WIP-transferred asset."
            )

        if not asset.wip_reference.approved:
            raise ValidationError(
                "WIP transfer must be approved before capitalization."
            )

    elif require_invoice:
        invoice_exists = asset.documents.filter(
            document_type=AssetDocument.DocumentType.INVOICE
        ).exists()

        if not invoice_exists:
            raise ValidationError(
                "Invoice attachment is required before capitalization."
            )

    if require_approval_document:
        approval_exists = asset.documents.filter(
            document_type=AssetDocument.DocumentType.APPROVAL
        ).exists()

        if not approval_exists:
            raise ValidationError(
                "Approval document is required before capitalization."
            )


def _validate_accounting_period(capitalization_date):
    period_start = getattr(
        settings,
        "FAR_ACCOUNTING_PERIOD_START",
        None,
    )

    period_end = getattr(
        settings,
        "FAR_ACCOUNTING_PERIOD_END",
        None,
    )

    if period_start and capitalization_date < period_start:
        raise ValidationError(
            "Capitalization date is outside the open accounting period."
        )

    if period_end and capitalization_date > period_end:
        raise ValidationError(
            "Capitalization date is outside the open accounting period."
        )


def validate_capitalization_eligibility(asset):

    if asset.is_deleted:
        raise ValidationError(
            "Deleted assets cannot be capitalized."
        )

    if asset.lifecycle_status != AssetCore.LifecycleStatus.DRAFT:
        raise ValidationError(
            "Only Draft assets can be capitalized."
        )

    if asset.validation_status == AssetCore.ValidationStatus.ERROR:
        raise ValidationError(
            "Asset has blocking validation errors."
        )

    if not asset.capitalization_eligible:
        raise ValidationError(
            "Asset is not eligible for capitalization."
        )

    if not hasattr(asset, "basic_info"):
        raise ValidationError(
            "Basic asset information is required."
        )

    if not hasattr(asset, "classification"):
        raise ValidationError(
            "Classification information is required."
        )

    if not hasattr(asset, "location_info"):
        raise ValidationError(
            "Location information is required."
        )

    if not hasattr(asset, "financial_info"):
        raise ValidationError(
            "Financial information is required."
        )

    if not hasattr(asset, "responsibility"):
        raise ValidationError(
            "Responsibility information is required."
        )

    basic = asset.basic_info
    classification = asset.classification
    location = asset.location_info
    financial = asset.financial_info

    validate_positive_quantity(basic.quantity)
    validate_positive_cost(financial.purchase_cost)

    if not basic.asset_name:
        raise ValidationError("Asset name is required.")

    if not basic.asset_type:
        raise ValidationError("Asset type is required.")

    if not basic.unit_of_measure:
        raise ValidationError("Unit of measure is required.")

    if not classification.asset_class:
        raise ValidationError("Asset class is required.")

    if not classification.asset_category:
        raise ValidationError("Asset category is required.")

    if not location.company_legal_entity:
        raise ValidationError(
            "Company/legal entity is required."
        )

    if not financial.currency:
        raise ValidationError("Currency is required.")

    if financial.total_capitalizable_cost <= 0:
        raise ValidationError(
            "Total capitalizable cost must be greater than zero."
        )

    if not financial.capitalization_date:
        raise ValidationError(
            "Capitalization date is required."
        )

    if not financial.gl_asset_account:
        raise ValidationError(
            "GL asset account is required."
        )

    _require_depreciation_fields(asset)
    _validate_source_evidence(asset)
    _validate_accounting_period(
        financial.capitalization_date
    )

    require_approval_workflow = getattr(
        settings,
        "FAR_REQUIRE_APPROVAL_WORKFLOW",
        False,
    )

    if require_approval_workflow:
        if asset.approval_status != AssetCore.ApprovalStatus.APPROVED:
            raise ValidationError(
                "Asset approval is required before capitalization."
            )

    if financial.capitalization_date > timezone.localdate():
        raise ValidationError(
            "Capitalization date cannot be in the future."
        )