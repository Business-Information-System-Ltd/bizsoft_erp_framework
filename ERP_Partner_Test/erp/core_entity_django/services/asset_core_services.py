from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from core_entity_django.constants.constants import ActionType, SourceType

from core_entity_django.models import (
    AssetCore,
    AssetBasicInfo,
    AssetClassification,
    AssetLocationInfo,
    AssetFinancialInfo,
    AssetSupplierAcquisition,
    AssetResponsibility,
    AssetAuditLog,
    CapitalizationTransaction,
)

from core_entity_django.domain_policies.asset_core_domain_policy import (
    validate_draft_editable,
    validate_draft_deletable,
    validate_capitalization_eligibility,
    validate_positive_quantity,
    validate_positive_cost,
    validate_useful_life,
    validate_warranty_dates,
)

from core_entity_django.repositories.asset_core_repository import (
    AssetRepository,
)


def _snapshot(asset):

    data = {
        "id": asset.id,
        "draft_asset_number": asset.draft_asset_number,
        "asset_code": asset.asset_code,
        "lifecycle_status": asset.lifecycle_status,
        "validation_status": asset.validation_status,
        "capitalization_eligible": asset.capitalization_eligible,
        "approval_status": asset.approval_status,
        "is_deleted": asset.is_deleted,
    }

    if hasattr(asset, "basic_info"):
        data["asset_name"] = asset.basic_info.asset_name
        data["serial_number"] = asset.basic_info.serial_number
        data["quantity"] = str(asset.basic_info.quantity)

    if hasattr(asset, "financial_info"):
        data["purchase_cost"] = str(
            asset.financial_info.purchase_cost
        )
        data["total_capitalizable_cost"] = str(
            asset.financial_info.total_capitalizable_cost
        )

    return data


def _audit(
    *,
    asset,
    user,
    action_type,
    old_value=None,
    new_value=None,
    reason="",
    batch_number="",
    source_ip=None,
    device="",
):
    AssetAuditLog.objects.create(
        asset=asset,
        action_type=action_type,
        user=user,
        old_value=old_value,
        new_value=new_value,
        reason=reason,
        batch_number=batch_number,
        source_ip=source_ip,
        device=device,
    )


def _calculate_totals(financial):

    purchase_cost = (
        Decimal(str(financial.purchase_cost))
        if financial.purchase_cost is not None
        else Decimal("0.00")
    )

    other_cost = (
        Decimal(
            str(financial.other_directly_attributable_cost)
        )
        if financial.other_directly_attributable_cost is not None
        else Decimal("0.00")
    )

    financial.total_capitalizable_cost = (
        purchase_cost + other_cost
    )

    if financial.exchange_rate is not None:
        exchange_rate = Decimal(
            str(financial.exchange_rate)
        )

        financial.functional_currency_amount = (
            financial.total_capitalizable_cost
            * exchange_rate
        )
    else:
        financial.functional_currency_amount = None

    return financial


def _validate_asset_data(asset):

    errors = []
    warnings = []

    if not hasattr(asset, "basic_info"):
        errors.append(
            "Basic asset information is required."
        )
    else:
        basic = asset.basic_info

        if not basic.asset_name:
            errors.append(
                "Asset name is required."
            )

        if not basic.asset_type:
            errors.append(
                "Asset type is required."
            )

        if not basic.unit_of_measure:
            errors.append(
                "Unit of measure is required."
            )

        try:
            validate_positive_quantity(
                basic.quantity
            )
        except ValidationError as exc:
            errors.extend(exc.messages)

    if not hasattr(asset, "classification"):
        errors.append(
            "Classification information is required."
        )
    else:
        classification = asset.classification

        if not classification.asset_class:
            errors.append(
                "Asset class is required."
            )

        if not classification.asset_category:
            errors.append(
                "Asset category is required."
            )

        try:
            validate_useful_life(
                classification.useful_life
            )
        except ValidationError as exc:
            errors.extend(exc.messages)

        if (
            classification.depreciation_policy_group
            and not classification.useful_life
        ):
            errors.append(
                "Useful life is required for depreciable asset."
            )

        if (
            classification.depreciation_policy_group
            and not classification.depreciation_method
        ):
            errors.append(
                "Depreciation method is required."
            )

    if not hasattr(asset, "location_info"):
        errors.append(
            "Location information is required."
        )
    elif not asset.location_info.legal_entity_id:
        errors.append(
            "Company/legal entity is required."
        )

    if not hasattr(asset, "financial_info"):
        errors.append(
            "Financial information is required."
        )
    else:
        financial = asset.financial_info

        if not financial.currency:
            errors.append(
                "Currency is required."
            )

        try:
            validate_positive_cost(
                financial.purchase_cost
            )
        except ValidationError as exc:
            errors.extend(exc.messages)

        try:
            if (
                financial.other_directly_attributable_cost
                and financial.other_directly_attributable_cost < 0
            ):
                raise ValidationError(
                    "Other directly attributable cost cannot be negative."
                )
        except ValidationError as exc:
            errors.extend(exc.messages)

        if (
            financial.exchange_rate is not None
            and financial.exchange_rate <= 0
        ):
            errors.append(
                "Exchange rate must be greater than zero."
            )

        if not financial.capitalization_date:
            warnings.append(
                "Capitalization date has not been entered."
            )

        if not financial.gl_asset_account_id:
            warnings.append(
                "GL asset account has not been entered."
            )

    if not hasattr(asset, "responsibility"):
        errors.append(
            "Responsibility information is required."
        )

    if hasattr(asset, "supplier_info"):
        try:
            validate_warranty_dates(
                asset.supplier_info.warranty_start_date,
                asset.supplier_info.warranty_end_date,
            )
        except ValidationError as exc:
            errors.extend(exc.messages)

    if (
        hasattr(asset, "basic_info")
        and asset.basic_info.serial_number
    ):
        duplicate = (
            AssetBasicInfo.objects
            .filter(
                serial_number=asset.basic_info.serial_number
            )
            .exclude(asset_id=asset.id)
            .exists()
        )

        if duplicate:
            errors.append(
                "Duplicate serial number exists."
            )

    return errors, warnings


@transaction.atomic
def create_asset(
    *,
    user,
    validated_data,
    source_ip=None,
    device="",
    batch_number="",
):

    asset = AssetRepository.create_core(
        user=user,
        draft_date=validated_data["draft_date"],
        entry_source=validated_data.get(
            "entry_source",
            SourceType.MANUAL,
        ),
    )

    asset.remarks = validated_data.get(
        "remarks",
        "",
    )

    asset.save(
        update_fields=[
            "remarks",
            "last_updated_date",
        ]
    )

    AssetBasicInfo.objects.create(
        asset=asset,
        **validated_data["basic_info"],
    )

    AssetClassification.objects.create(
        asset=asset,
        **validated_data["classification"],
    )

    AssetLocationInfo.objects.create(
        asset=asset,
        **validated_data["location_info"],
    )

    financial = AssetFinancialInfo.objects.create(
        asset=asset,
        **validated_data["financial_info"],
    )

    _calculate_totals(financial)
    financial.save()

    AssetSupplierAcquisition.objects.create(
        asset=asset,
        **validated_data.get("supplier_info", {}),
    )

    AssetResponsibility.objects.create(
        asset=asset,
        **validated_data.get("responsibility", {}),
    )

    _audit(
        asset=asset,
        user=user,
        action_type=ActionType.CREATE,
        new_value=_snapshot(asset),
        batch_number=batch_number,
        source_ip=source_ip,
        device=device,
    )

    return asset


@transaction.atomic
def update_asset(
    *,
    asset,
    user,
    validated_data,
    source_ip=None,
    device="",
):

    validate_draft_editable(asset)

    old_value = _snapshot(asset)

    if "draft_date" in validated_data:
        asset.draft_date = validated_data["draft_date"]

    if "remarks" in validated_data:
        asset.remarks = validated_data["remarks"]

    relation_map = {
        "basic_info": "basic_info",
        "classification": "classification",
        "location_info": "location_info",
        "financial_info": "financial_info",
        "supplier_info": "supplier_info",
        "responsibility": "responsibility",
    }

    for field_name, values in validated_data.items():

        relation_name = relation_map.get(field_name)

        if not relation_name:
            continue

        related = getattr(
            asset,
            relation_name,
            None,
        )

        if related is None:
            continue

        for key, value in values.items():

            if key in (
                "total_capitalizable_cost",
                "functional_currency_amount",
            ):
                continue

            setattr(
                related,
                key,
                value,
            )

        if field_name == "financial_info":
            _calculate_totals(related)

        related.save()

    asset.validation_status = (
        AssetCore.ValidationStatus.INCOMPLETE
    )

    asset.capitalization_eligible = False

    asset.approval_status = (
        AssetCore.ApprovalStatus.NOT_SUBMITTED
    )

    asset.last_updated_by = user

    asset.save()

    _audit(
        asset=asset,
        user=user,
        action_type=AssetAuditLog.ActionType.EDIT,
        old_value=old_value,
        new_value=_snapshot(asset),
        source_ip=source_ip,
        device=device,
    )

    return asset


@transaction.atomic
def validate_asset(
    *,
    asset,
    user,
    source_ip=None,
    device="",
):

    if asset.is_deleted:
        raise ValidationError(
            "Deleted asset cannot be validated."
        )

    errors, warnings = _validate_asset_data(
        asset
    )

    if errors:
        asset.validation_status = (
            AssetCore.ValidationStatus.ERROR
        )
        asset.capitalization_eligible = False

    elif warnings:
        asset.validation_status = (
            AssetCore.ValidationStatus.WARNING
        )

        asset.capitalization_eligible = True

    else:
        asset.validation_status = (
            AssetCore.ValidationStatus.COMPLETE
        )

        asset.capitalization_eligible = True

    asset.last_updated_by = user

    asset.save(
        update_fields=[
            "validation_status",
            "capitalization_eligible",
            "last_updated_by",
            "last_updated_date",
        ]
    )

    _audit(
        asset=asset,
        user=user,
        action_type=AssetAuditLog.ActionType.VALIDATE,
        new_value={
            "validation_status": asset.validation_status,
            "capitalization_eligible": asset.capitalization_eligible,
            "errors": errors,
            "warnings": warnings,
        },
        source_ip=source_ip,
        device=device,
    )

    return {
        "asset": asset,
        "errors": errors,
        "warnings": warnings,
    }


@transaction.atomic
def delete_asset(
    *,
    asset,
    user,
    reason,
    source_ip=None,
    device="",
):

    validate_draft_deletable(asset)

    old_value = _snapshot(asset)

    AssetRepository.soft_delete(
        asset,
        user=user,
        reason=reason,
    )

    _audit(
        asset=asset,
        user=user,
        action_type=AssetAuditLog.ActionType.DELETE,
        old_value=old_value,
        new_value={
            "is_deleted": True,
            "deletion_reason": reason,
        },
        reason=reason,
        source_ip=source_ip,
        device=device,
    )

    return asset


@transaction.atomic
def capitalize_asset(
    *,
    asset,
    user,
    source_ip=None,
    device="",
):

    validate_capitalization_eligibility(asset)

    financial = asset.financial_info

    if not asset.asset_code:
        asset.asset_code = (
            AssetRepository.generate_asset_code()
        )

    transaction_reference = (
        f"CAP-{asset.draft_asset_number}"
    )

    capitalization = (
        CapitalizationTransaction.objects.create(
            asset=asset,
            capitalization_date=financial.capitalization_date,
            amount=financial.total_capitalizable_cost,
            currency=financial.currency,
            gl_asset_account=financial.gl_asset_account,
            transaction_reference=transaction_reference,
            capitalized_by=user,
        )
    )

    old_value = _snapshot(asset)

    asset.lifecycle_status = (
        AssetCore.LifecycleStatus.CAPITALIZED
    )

    asset.capitalization_eligible = False
    asset.last_updated_by = user

    asset.save()

    _audit(
        asset=asset,
        user=user,
        action_type=AssetAuditLog.ActionType.CAPITALIZE,
        old_value=old_value,
        new_value=_snapshot(asset),
        source_ip=source_ip,
        device=device,
    )

    return capitalization