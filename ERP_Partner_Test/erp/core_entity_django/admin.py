from django.contrib import admin

from erp_partners.models.partner import Partner
from core_entity_django.models import (
    AssetCore,
    AssetBasicInfo,
    AssetClassification,
    AssetLocationInfo,
    AssetFinancialInfo,
    AssetSupplierAcquisition,
    AssetResponsibility,
    AssetDocument,
    AssetImportBatch,
    AssetImportError,
    AssetWipReference,
    AssetAuditLog,
    CapitalizationTransaction,
)


@admin.register(AssetCore)
class AssetCoreAdmin(admin.ModelAdmin):

    list_display = (
        "draft_asset_number",
        "asset_code",
        "draft_date",
        "entry_source",
        "lifecycle_status",
        "validation_status",
        "capitalization_eligible",
        "approval_status",
        "is_deleted",
    )

    list_filter = (
        "lifecycle_status",
        "validation_status",
        "entry_source",
        "approval_status",
        "is_deleted",
    )

    search_fields = (
        "draft_asset_number",
        "asset_code",
    )


@admin.register(AssetBasicInfo)
class AssetBasicInfoAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "asset_name",
        "serial_number",
        "quantity",
        "asset_type",
    )

    search_fields = (
        "asset_name",
        "serial_number",
    )


@admin.register(AssetClassification)
class AssetClassificationAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "asset_class",
        "asset_category",
        "asset_subcategory",
    )


@admin.register(AssetLocationInfo)
class AssetLocationInfoAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "legal_entity_id",
        "branch_id",
        "department_id",
        "location_id",
        "current_physical_status",
    )


@admin.register(AssetFinancialInfo)
class AssetFinancialInfoAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "acquisition_date",
        "invoice_number",
        "purchase_cost",
        "total_capitalizable_cost",
        "gl_asset_account_id",
        "capitalization_date",
    )


@admin.register(AssetSupplierAcquisition)
class AssetSupplierAcquisitionAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "supplier_display",
        "supplier_code_display",
        "procurement_method",
        "contract_number",
        "warranty_start_date",
        "warranty_end_date",
    )

    @admin.display(
        description="Supplier"
    )
    def supplier_display(self, obj):
        if not obj.supplier_partner_id:
            return "-"

        partner = (
            Partner.objects
            .filter(id=obj.supplier_partner_id)
            .first()
        )

        return (
            partner.display_name
            if partner
            else "-"
        )

    @admin.display(
        description="Supplier Code"
    )
    def supplier_code_display(self, obj):
        if not obj.supplier_partner_id:
            return "-"

        partner = (
            Partner.objects
            .filter(id=obj.supplier_partner_id)
            .first()
        )

        return (
            partner.partner_code
            if partner
            else "-"
        )


@admin.register(AssetResponsibility)
class AssetResponsibilityAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "responsible_department_id",
        "custodian_partner_id",
        "asset_controller_partner_id",
        "assigned_user_partner_id",
    )


@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "document_type",
        "reference_number",
        "uploaded_by",
        "uploaded_at",
    )


@admin.register(AssetImportBatch)
class AssetImportBatchAdmin(admin.ModelAdmin):

    list_display = (
        "batch_number",
        "file_name",
        "file_type",
        "status",
        "total_rows",
        "valid_rows",
        "error_rows",
    )


@admin.register(AssetImportError)
class AssetImportErrorAdmin(admin.ModelAdmin):

    list_display = (
        "batch",
        "row_number",
        "field_name",
        "error_code",
        "corrected",
    )


@admin.register(AssetWipReference)
class AssetWipReferenceAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "wip_item_reference",
        "wip_project_reference",
        "allocated_amount",
        "approved",
    )


@admin.register(AssetAuditLog)
class AssetAuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "action_type",
        "user",
        "timestamp",
        "batch_number",
    )

    list_filter = (
        "action_type",
    )


@admin.register(CapitalizationTransaction)
class CapitalizationTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "capitalization_date",
        "amount",
        "currency",
        "transaction_reference",
        "capitalized_by",
    )