from django.db import transaction

from core_entity_django.models import AssetCore
from core_entity_django.constants.constants import (LifecycleStatus, ValidationStatus, ApprovalStatus)

class AssetRepository:

    @staticmethod
    def _next_draft_number():
        last = (
            AssetCore.objects
            .filter(draft_asset_number__startswith="DRAFT-")
            .order_by("-id")
            .first()
        )

        if not last:
            number = 1
        else:
            try:
                number = (
                    int(last.draft_asset_number.split("-")[-1])
                    + 1
                )
            except (ValueError, IndexError):
                number = AssetCore.objects.count() + 1

        return f"DRAFT-{number:06d}"

    @staticmethod
    def _next_asset_code():
        last = (
            AssetCore.objects
            .filter(asset_code__startswith="FA-")
            .order_by("-id")
            .first()
        )

        if not last:
            number = 1
        else:
            try:
                number = (
                    int(last.asset_code.split("-")[-1])
                    + 1
                )
            except (ValueError, IndexError):
                number = AssetCore.objects.count() + 1

        return f"FA-{number:06d}"

    @classmethod
    @transaction.atomic
    def create_core(
        cls,
        *,
        user,
        draft_date,
        entry_source,
    ):
        return AssetCore.objects.create(
            draft_asset_number=cls._next_draft_number(),
            draft_date=draft_date,
            entry_source=entry_source,
            lifecycle_status=LifecycleStatus.DRAFT,
            validation_status=ValidationStatus.INCOMPLETE,
            capitalization_eligible=False,
            approval_status=ApprovalStatus.NOT_SUBMITTED,
            prepared_by=user,
            last_updated_by=user,
        )

    @classmethod
    @transaction.atomic
    def generate_asset_code(cls, asset):
        if not asset.asset_code:
            asset.asset_code = cls._next_asset_code()
            asset.save(
                update_fields=[
                    "asset_code",
                ]
            )

        return asset

    @staticmethod
    def save(instance, *, user):
        instance.last_updated_by = user
        instance.save()
        return instance

    @staticmethod
    def soft_delete(instance, *, user):
        instance.is_deleted = True
        instance.last_updated_by = user

        instance.save(
            update_fields=[
                "is_deleted",
                "last_updated_by",
                "last_updated_date",
            ]
        )

        return instance