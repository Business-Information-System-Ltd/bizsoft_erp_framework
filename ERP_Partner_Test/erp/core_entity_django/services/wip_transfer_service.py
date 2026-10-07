from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from core_entity_django.models import (
    AssetCore,
    AssetWipReference,
    AssetAuditLog,
)

from core_entity_django.services.asset_core_services import (
    create_asset,
)


@transaction.atomic
def transfer_wip_to_assets(
    *,
    user,
    validated_data,
    source_ip=None,
    device="",
):

    source_balance = Decimal(
        validated_data["source_balance"]
    )

    allocations = validated_data["allocations"]

    total_allocated = sum(
        Decimal(item["allocated_amount"])
        for item in allocations
    )

    if total_allocated <= 0:
        raise ValidationError(
            "Total WIP allocation must be greater than zero."
        )

    if total_allocated > source_balance:
        raise ValidationError(
            "Total allocated amount cannot exceed available WIP balance."
        )

    if not validated_data["approved"]:
        raise ValidationError(
            "WIP transfer must be approved."
        )

    created_assets = []

    remaining_balance = source_balance

    for item in allocations:

        allocated_amount = Decimal(
            item["allocated_amount"]
        )

        if allocated_amount <= 0:
            raise ValidationError(
                "WIP allocation amount must be greater than zero."
            )

        if allocated_amount > remaining_balance:
            raise ValidationError(
                "WIP allocation exceeds remaining balance."
            )

        asset_data = {
            "draft_date": validated_data["transfer_date"],
            "entry_source": (
                AssetCore.SourceType.WIP_TRANSFER
            ),
            "remarks": item.get(
                "remarks",
                "",
            ),
            "basic_info": {
                "asset_name": item["asset_name"],
                "asset_description": item.get(
                    "asset_description",
                    "",
                ),
                "quantity": item["quantity"],
                "unit_of_measure": item["unit_of_measure"],
                "asset_type": item["asset_type"],
                "component_flag": False,
            },
            "classification": {
                "asset_class": item["asset_class"],
                "asset_category": item["asset_category"],
            },
            "location_info": {
                "company_legal_entity": item[
                    "company_legal_entity"
                ],
            },
            "financial_info": {
                "purchase_cost": allocated_amount,
                "other_directly_attributable_cost": Decimal(
                    "0.00"
                ),
                "currency": item["currency"],
            },
            "supplier_info": {},
            "responsibility": {
                "responsible_department": item.get(
                    "responsible_department",
                    "",
                ),
            },
        }

        asset = create_asset(
            user=user,
            validated_data=asset_data,
            source_ip=source_ip,
            device=device,
        )

        remaining_after = (
            remaining_balance - allocated_amount
        )

        AssetWipReference.objects.create(
            asset=asset,
            wip_item_reference=validated_data[
                "wip_item_reference"
            ],
            wip_project_reference=validated_data.get(
                "wip_project_reference",
                "",
            ),
            allocated_amount=allocated_amount,
            source_balance_before=remaining_balance,
            source_balance_after=remaining_after,
            transfer_date=validated_data[
                "transfer_date"
            ],
            approved=True,
        )

        AssetAuditLog.objects.create(
            asset=asset,
            action_type=AssetAuditLog.ActionType.WIP_TRANSFER,
            user=user,
            new_value={
                "wip_item_reference": validated_data[
                    "wip_item_reference"
                ],
                "allocated_amount": str(
                    allocated_amount
                ),
                "source_balance_before": str(
                    remaining_balance
                ),
                "source_balance_after": str(
                    remaining_after
                ),
            },
            source_ip=source_ip,
            device=device,
        )

        created_assets.append(asset)

        remaining_balance = remaining_after

    return {
        "assets": created_assets,
        "total_allocated": total_allocated,
        "remaining_balance": remaining_balance,
    }