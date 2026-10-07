from rest_framework import serializers

from erp_partners.models import Partner

from core_entity_django.constants.constants import SourceType

from core_entity_django.models import (
    AssetCore,
    AssetBasicInfo,
    AssetClassification,
    AssetLocationInfo,
    AssetFinancialInfo,
    AssetSupplierAcquisition,
    AssetResponsibility,
    AssetDocument,
)


class AssetBasicInfoSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AssetBasicInfo

        fields = [
            "asset_name",
            "asset_description",
            "asset_type",
            "brand",
            "model",
            "serial_number",
            "quantity",
            "unit_of_measure",
        ]


class AssetClassificationSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AssetClassification

        fields = [
            "asset_class",
            "asset_category",
            "asset_subcategory",
            "depreciation_method",
            "useful_life",
            "residual_value",
        ]


class AssetLocationSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AssetLocationInfo

        fields = [
            "legal_entity_id",
            "branch_id",
            "department_id",
            "location_id",
            "building_floor_room",
            "rack_space_area",
            "current_physical_status",
        ]


class AssetFinancialSerializer(
    serializers.ModelSerializer
):

    total_capitalizable_cost = (
        serializers.DecimalField(
            max_digits=20,
            decimal_places=2,
            read_only=True,
        )
    )

    functional_currency_amount = (
        serializers.DecimalField(
            max_digits=20,
            decimal_places=2,
            read_only=True,
        )
    )

    class Meta:
        model = AssetFinancialInfo

        fields = [
            "acquisition_date",
            "invoice_date",
            "invoice_number",
            "purchase_order_number",
            "purchase_cost",
            "other_directly_attributable_cost",
            "total_capitalizable_cost",
            "currency",
            "exchange_rate",
            "functional_currency_amount",
            "capitalization_date",
            "gl_asset_account_id",
            "accumulated_depreciation_account_id",
            "depreciation_expense_account_id",
            "cost_center_id",
        ]


class AssetSupplierSerializer(
    serializers.ModelSerializer
):

    supplier_name = serializers.SerializerMethodField()

    supplier_code = serializers.SerializerMethodField()

    class Meta:
        model = AssetSupplierAcquisition

        fields = [
            "supplier_partner_id",
            "supplier_name",
            "supplier_code",
            "procurement_method",
            "contract_number",
            "delivery_note_number",
            "warranty_start_date",
            "warranty_end_date",
            "warranty_provider_partner_id",
        ]

    def _get_partner(
        self,
        partner_id,
    ):
        if not partner_id:
            return None

        return Partner.objects.filter(
            id=partner_id,
        ).first()

    def get_supplier_name(
        self,
        obj,
    ):
        partner = self._get_partner(
            obj.supplier_partner_id
        )

        return (
            partner.display_name
            if partner
            else None
        )

    def get_supplier_code(
        self,
        obj,
    ):
        partner = self._get_partner(
            obj.supplier_partner_id
        )

        return (
            partner.partner_code
            if partner
            else None
        )


class AssetResponsibilitySerializer(
    serializers.ModelSerializer
):

    custodian_name = serializers.SerializerMethodField()

    custodian_code = serializers.SerializerMethodField()

    class Meta:
        model = AssetResponsibility

        fields = [
            "responsible_department_id",
            "custodian_partner_id",
            "custodian_name",
            "custodian_code",
            "asset_controller_partner_id",
            "assigned_user_partner_id",
        ]

    def _get_partner(
        self,
        partner_id,
    ):
        if not partner_id:
            return None

        return Partner.objects.filter(
            id=partner_id,
        ).first()

    def get_custodian_name(
        self,
        obj,
    ):
        partner = self._get_partner(
            obj.custodian_partner_id
        )

        return (
            partner.display_name
            if partner
            else None
        )

    def get_custodian_code(
        self,
        obj,
    ):
        partner = self._get_partner(
            obj.custodian_partner_id
        )

        return (
            partner.partner_code
            if partner
            else None
        )


class AssetDocumentSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AssetDocument

        fields = [
            "id",
            "document_type",
            "file",
            "reference_number",
            "remarks",
            "uploaded_by",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_at",
        ]

class AssetCoreSerializer(
    serializers.ModelSerializer
):

    basic_info = AssetBasicInfoSerializer(
        read_only=True
    )

    classification = AssetClassificationSerializer(
        read_only=True
    )

    location_info = AssetLocationSerializer(
        read_only=True
    )

    financial_info = AssetFinancialSerializer(
        read_only=True
    )

    supplier_info = AssetSupplierSerializer(
        read_only=True
    )

    responsibility = AssetResponsibilitySerializer(
        read_only=True
    )

    documents = AssetDocumentSerializer(
        many=True,
        read_only=True,
    )

    # prepared_by_name = serializers.CharField(
    #     source="prepared_by.get_username",
    #     read_only=True,
    # )

    # last_updated_by_name = serializers.CharField(
    #     source="last_updated_by.get_username",
    #     read_only=True,
    # )

    class Meta:
        model = AssetCore

        fields = [
            "id",
            "draft_asset_number",
            "asset_code",
            "draft_date",
            "entry_source",
            "lifecycle_status",
            "validation_status",
            "capitalization_eligible",
            "approval_status",
            # "is_deleted",
            # "deleted_at",
            # "deletion_reason",
            "remarks",
            # "approval_print_count",
            # "last_printed_at",
            # "prepared_by",
            # "prepared_by_name",
            # "last_updated_by",
            # "last_updated_by_name",
            # "last_updated_date",
            # "created_at",
            "basic_info",
            "classification",
            "location_info",
            "financial_info",
            "supplier_info",
            "responsibility",
            "documents",
        ]

        read_only_fields = [
            "draft_asset_number",
            "asset_code",
            "lifecycle_status",
            "validation_status",
            "capitalization_eligible",
            "approval_status",
            # "is_deleted",
            # "deleted_at",
            # "deletion_reason",
            # "approval_print_count",
            # "last_printed_at",
            # "prepared_by",
            # "last_updated_by",
            # "last_updated_date",
            # "created_at",
        ]


class AssetCreateSerializer(serializers.Serializer):

    draft_date = serializers.DateField()

    entry_source = serializers.ChoiceField(
        choices=SourceType.choices,
        default=SourceType.MANUAL,
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    basic_info = serializers.DictField()

    classification = serializers.DictField()

    location_info = serializers.DictField()

    financial_info = serializers.DictField()

    supplier_info = serializers.DictField(
        required=False,
        default=dict,
    )

    responsibility = serializers.DictField(
        required=False,
        default=dict,
    )

    def validate(self, attrs):

        supplier_id = (
            attrs
            .get("supplier_info", {})
            .get("supplier_partner_id")
        )

        if supplier_id:

            valid_supplier = (
                Partner.objects
                .filter(
                    id=supplier_id,
                    is_active=True,
                    roles__role_type="SUPPLIER",
                    roles__status="ACTIVE",
                )
                .exists()
            )

            if not valid_supplier:
                raise serializers.ValidationError({
                    "supplier_info": {
                        "supplier_partner_id":
                            "Selected partner is not an active supplier."
                    }
                })

        custodian_id = (
            attrs
            .get("responsibility", {})
            .get("custodian_partner_id")
        )

        if custodian_id:

            valid_custodian = (
                Partner.objects
                .filter(
                    id=custodian_id,
                    is_active=True,
                    roles__role_type="ASSET_CUSTODIAN",
                    roles__status="ACTIVE",
                )
                .exists()
            )

            if not valid_custodian:
                raise serializers.ValidationError({
                    "responsibility": {
                        "custodian_partner_id":
                            "Selected partner is not an active asset custodian."
                    }
                })

        return attrs

class AssetUpdateSerializer(serializers.Serializer):

    draft_date = serializers.DateField(
        required=False
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    basic_info = AssetBasicInfoSerializer(
        required=False
    )

    classification = AssetClassificationSerializer(
        required=False
    )

    location_info = AssetLocationSerializer(
        required=False
    )

    financial_info = AssetFinancialSerializer(
        required=False
    )

    supplier_info = AssetSupplierSerializer(
        required=False
    )

    responsibility = AssetResponsibilitySerializer(
        required=False
    )


class DeleteAssetSerializer(serializers.Serializer):

    reason = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    confirm = serializers.BooleanField(
        required=True,
    )

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError(
                "Deletion confirmation is required."
            )
        return value


class BulkAssetSerializer(serializers.Serializer):

    asset_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )


class BulkDeleteSerializer(BulkAssetSerializer):

    reason = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    confirm = serializers.BooleanField(
        required=True,
    )

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError(
                "Deletion confirmation is required."
            )
        return value


class BulkCapitalizeSerializer(BulkAssetSerializer):
    confirmation = serializers.BooleanField(
        required=True
    )

    def validate_confirmation(self, value):
        if not value:
            raise serializers.ValidationError(
                "Capitalization confirmation is required."
            )
        return value


class ApprovalActionSerializer(serializers.Serializer):

    action = serializers.ChoiceField(
        choices=[
            ("APPROVE", "Approve"),
            ("REJECT", "Reject"),
        ]
    )

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class ImportAssetSerializer(serializers.Serializer):

    file = serializers.FileField()

    template_version = serializers.CharField(
        required=True
    )


class WipTransferItemSerializer(serializers.Serializer):

    asset_name = serializers.CharField()

    asset_description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    asset_type = serializers.CharField()

    quantity = serializers.DecimalField(
        max_digits=18,
        decimal_places=4,
    )

    unit_of_measure = serializers.CharField()

    asset_class = serializers.CharField()

    asset_category = serializers.CharField()

    company_legal_entity = serializers.CharField()

    responsible_department = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    allocated_amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    currency = serializers.CharField()

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class WipTransferSerializer(serializers.Serializer):

    wip_item_reference = serializers.CharField()

    wip_project_reference = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    source_balance = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    transfer_date = serializers.DateField()

    approved = serializers.BooleanField()

    allocations = WipTransferItemSerializer(
        many=True,
        allow_empty=False,
    )