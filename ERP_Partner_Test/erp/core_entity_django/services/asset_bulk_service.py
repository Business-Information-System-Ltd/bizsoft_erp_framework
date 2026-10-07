from django.core.exceptions import ValidationError
from django.db import transaction

from core_entity_django.models import AssetAuditLog

from core_entity_django.services.asset_core_services import (
    validate_asset,
    delete_asset,
)


@transaction.atomic
def bulk_validate(
    *,
    assets,
    user,
    source_ip=None,
    device="",
):

    results = []

    for asset in assets:

        try:
            result = validate_asset(
                asset=asset,
                user=user,
                source_ip=source_ip,
                device=device,
            )

            results.append({
                "asset_id": asset.id,
                "status": "SUCCESS",
                "validation_status": (
                    result["asset"].validation_status
                ),
                "errors": result["errors"],
                "warnings": result["warnings"],
            })

        except ValidationError as exc:

            results.append({
                "asset_id": asset.id,
                "status": "ERROR",
                "errors": exc.messages,
            })

    return results


@transaction.atomic
def bulk_delete(
    *,
    assets,
    user,
    reason,
    source_ip=None,
    device="",
):

    results = []

    for asset in assets:

        try:
            delete_asset(
                asset=asset,
                user=user,
                reason=reason,
                source_ip=source_ip,
                device=device,
            )

            results.append({
                "asset_id": asset.id,
                "status": "DELETED",
            })

        except ValidationError as exc:

            results.append({
                "asset_id": asset.id,
                "status": "ERROR",
                "errors": exc.messages,
            })

    return results