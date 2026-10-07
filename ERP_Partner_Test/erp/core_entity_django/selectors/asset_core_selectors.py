from django.db.models import Q

from core_entity_django.models import AssetCore
from core_entity_django.constants.constants import LifecycleStatus


def get_asset(asset_id):

    return (
        AssetCore.objects
        .select_related(
            "prepared_by",
            "last_updated_by",
            "deleted_by",
            "last_printed_by",
            "basic_info",
            "classification",
            "location_info",
            "financial_info",
            "supplier_info",
            "responsibility",
            "wip_reference",
            "capitalization_transaction",
        )
        .prefetch_related(
            "documents",
            "audit_logs",
        )
        .filter(
            pk=asset_id,
            is_deleted=False,
        )
        .first()
    )


def list_draft_assets(filters=None):

    filters = filters or {}

    qs = (
        AssetCore.objects
        .select_related(
            "basic_info",
            "classification",
            "location_info",
            "financial_info",
            "supplier_info",
            "prepared_by",
        )
        .filter(
            lifecycle_status=LifecycleStatus.DRAFT,
            is_deleted=False,
        )
    )

    if filters.get("draft_date_from"):
        qs = qs.filter(
            draft_date__gte=filters["draft_date_from"]
        )

    if filters.get("draft_date_to"):
        qs = qs.filter(
            draft_date__lte=filters["draft_date_to"]
        )

    if filters.get("acquisition_date_from"):
        qs = qs.filter(
            financial_info__acquisition_date__gte=filters[
                "acquisition_date_from"
            ]
        )

    if filters.get("acquisition_date_to"):
        qs = qs.filter(
            financial_info__acquisition_date__lte=filters[
                "acquisition_date_to"
            ]
        )

    if filters.get("asset_class"):
        qs = qs.filter(
            classification__asset_class=filters["asset_class"]
        )

    if filters.get("asset_category"):
        qs = qs.filter(
            classification__asset_category=filters["asset_category"]
        )

    if filters.get("asset_type"):
        qs = qs.filter(
            basic_info__asset_type=filters["asset_type"]
        )

    if filters.get("source"):
        qs = qs.filter(
            entry_source=filters["source"]
        )

    if filters.get("company"):
        qs = qs.filter(
            location_info__company_legal_entity=filters["company"]
        )

    if filters.get("branch"):
        qs = qs.filter(
            location_info__branch=filters["branch"]
        )

    if filters.get("department"):
        qs = qs.filter(
            location_info__department=filters["department"]
        )

    if filters.get("supplier"):
        qs = qs.filter(
            supplier_info__supplier_name__icontains=filters["supplier"]
        )

    if filters.get("validation_status"):
        qs = qs.filter(
            validation_status=filters["validation_status"]
        )

    if filters.get("capitalization_eligible") is not None:
        qs = qs.filter(
            capitalization_eligible=filters[
                "capitalization_eligible"
            ]
        )

    if filters.get("prepared_by"):
        qs = qs.filter(
            prepared_by_id=filters["prepared_by"]
        )

    if filters.get("import_batch"):
        qs = qs.filter(
            audit_logs__batch_number=filters["import_batch"]
        )

    if filters.get("wip_reference"):
        qs = qs.filter(
            wip_reference__wip_item_reference__icontains=filters[
                "wip_reference"
            ]
        )

    if filters.get("keyword"):
        keyword = filters["keyword"]

        qs = qs.filter(
            Q(draft_asset_number__icontains=keyword)
            | Q(asset_code__icontains=keyword)
            | Q(basic_info__asset_name__icontains=keyword)
            | Q(basic_info__serial_number__icontains=keyword)
            | Q(financial_info__invoice_number__icontains=keyword)
            | Q(financial_info__purchase_order_number__icontains=keyword)
            | Q(supplier_info__supplier_name__icontains=keyword)
            | Q(wip_reference__wip_item_reference__icontains=keyword)
        )

    return qs.distinct()


def get_capitalization_candidates(asset_ids):

    return (
        AssetCore.objects
        .select_related(
            "basic_info",
            "classification",
            "location_info",
            "financial_info",
            "responsibility",
        )
        .filter(
            id__in=asset_ids,
            lifecycle_status=AssetCore.LifecycleStatus.DRAFT,
            is_deleted=False,
        )
    )