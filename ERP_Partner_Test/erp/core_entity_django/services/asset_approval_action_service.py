from django.core.exceptions import ValidationError
from django.db import transaction

from core_entity_django.models import (
    AssetCore,
    AssetAuditLog,
)


@transaction.atomic
def approval_action(
    *,
    asset,
    user,
    action,
    reason="",
    source_ip=None,
    device="",
):

    if asset.is_deleted:
        raise ValidationError(
            "Deleted asset cannot be approved."
        )

    if asset.lifecycle_status != AssetCore.LifecycleStatus.DRAFT:
        raise ValidationError(
            "Only Draft assets can be approved."
        )

    if action == "APPROVE":

        if asset.approval_status not in (
            AssetCore.ApprovalStatus.PRINTED,
            AssetCore.ApprovalStatus.REJECTED,
        ):
            raise ValidationError(
                "Approval document must be printed before approval."
            )

        old_status = asset.approval_status

        asset.approval_status = (
            AssetCore.ApprovalStatus.APPROVED
        )

        asset.last_updated_by = user
        asset.save()

        AssetAuditLog.objects.create(
            asset=asset,
            action_type=AssetAuditLog.ActionType.EDIT,
            user=user,
            old_value={
                "approval_status": old_status,
            },
            new_value={
                "approval_status": asset.approval_status,
            },
            reason=reason,
            source_ip=source_ip,
            device=device,
        )

        return asset

    if action == "REJECT":

        old_status = asset.approval_status

        asset.approval_status = (
            AssetCore.ApprovalStatus.REJECTED
        )

        asset.capitalization_eligible = False
        asset.last_updated_by = user
        asset.save()

        AssetAuditLog.objects.create(
            asset=asset,
            action_type=AssetAuditLog.ActionType.EDIT,
            user=user,
            old_value={
                "approval_status": old_status,
            },
            new_value={
                "approval_status": asset.approval_status,
            },
            reason=reason,
            source_ip=source_ip,
            device=device,
        )

        return asset

    raise ValidationError(
        "Invalid approval action."
    )