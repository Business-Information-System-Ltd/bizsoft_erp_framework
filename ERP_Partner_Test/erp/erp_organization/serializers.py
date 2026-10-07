# """
# BizSoft ERP - ERP Organization

# Company: Business Information Systems Ltd. / BizSoft
# Author: Business Information Systems Ltd. / BizSoft
# Package: erp_organization
# Version: 1.0.0

# Purpose:
# This file is part of the erp_organization ERP business foundation package.

# Important:
# - This package defines legal entities, branches, departments, SBUs, facilities,
#   warehouses, projects, cost centers, profit centers, physical locations,
#   custodians, and flexible organization relationships.
# - Organization tells where and who.
# - Dimension tells how to classify, summarize, analyze, and report.
# - Do not implement accounting posting, inventory movement, FAR depreciation,
#   payroll, workflow routing, permission engine, audit trail, or notifications.
# - core_* packages must not depend on erp_organization.

# Rule:
# Selectors read data.
# Domain Policies validate domain truth.
# Application Policies validate whether an action is allowed in context.
# Application Services orchestrate use cases.

# File Purpose:
# Defines DRF serializers for organization models.
# """


# try:
#     from rest_framework import serializers
#     from erp_organization.models import *
#     class OrganizationUnitSerializer(serializers.ModelSerializer):
#         class Meta: model=OrganizationUnit; fields='__all__'
#     class LegalEntityProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=LegalEntityProfile; fields='__all__'
#     class BranchProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=BranchProfile; fields='__all__'
#     class DepartmentProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=DepartmentProfile; fields='__all__'
#     class StrategicBusinessUnitProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=StrategicBusinessUnitProfile; fields='__all__'
#     class CostCenterProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=CostCenterProfile; fields='__all__'
#     class ProfitCenterProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=ProfitCenterProfile; fields='__all__'
#     class PhysicalLocationProfileSerializer(serializers.ModelSerializer):
#         class Meta: model=PhysicalLocationProfile; fields='__all__'
#     class CustodianAssignmentSerializer(serializers.ModelSerializer):
#         class Meta: model=CustodianAssignment; fields='__all__'
#     class OrganizationRelationshipSerializer(serializers.ModelSerializer):
#         class Meta: model=OrganizationRelationship; fields='__all__'
# except Exception:
#     OrganizationUnitSerializer=LegalEntityProfileSerializer=BranchProfileSerializer=DepartmentProfileSerializer=StrategicBusinessUnitProfileSerializer=CostCenterProfileSerializer=ProfitCenterProfileSerializer=PhysicalLocationProfileSerializer=CustodianAssignmentSerializer=OrganizationRelationshipSerializer=None

"""BizSoft ERP - ERP Organization serializers."""
from rest_framework import serializers
from erp_organization.models import (
    OrganizationUnit, LegalEntityProfile, Region, Zone, Address, BranchProfile,
    DepartmentProfile, StrategicBusinessUnitProfile, CostCenterProfile,
    ProfitCenterProfile, PhysicalLocationProfile, CustodianAssignment,
    OrganizationRelationship,
)

class OrganizationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUnit
        fields = "__all__"

class LegalEntityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntityProfile
        fields = "__all__"

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "id",
            "region_code",
            "region_name",
            "timezone_name",
            "is_active",
            'map_latitude',   
            'map_longitude',
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = [
            "id",
            "zone_code",
            "zone_name",
            "region",
            "timezone_abbreviation",
            "utc_offset",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
    def validate(self, attrs):
        region = attrs.get("region", getattr(self.instance, "region", None))
        if region and not region.is_active:
            raise serializers.ValidationError({"region": "Selected region is inactive."})
        return attrs

class AddressSerializer(serializers.ModelSerializer):
    region_detail = RegionSerializer(source="region", read_only=True)
    zone_detail = ZoneSerializer(source="zone", read_only=True)

    class Meta:
        model = Address
        fields = [
            "id", "address_line_1", "address_line_2", "township", "city",
            "region", "region_detail", "zone", "zone_detail", "postal_code",
             "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        region = attrs.get("region", getattr(self.instance, "region", None))
        zone = attrs.get("zone", getattr(self.instance, "zone", None))
        if region and not region.is_active:
            raise serializers.ValidationError({"region": "Selected region is inactive."})
        if zone and not zone.is_active:
            raise serializers.ValidationError({"zone": "Selected zone is inactive."})
        if region and zone and zone.region_id != region.id:
            raise serializers.ValidationError({"zone": "Selected zone does not belong to selected region."})
        return attrs

class BranchProfileSerializer(serializers.ModelSerializer):
    region_detail = RegionSerializer(source="region", read_only=True)
    zone_detail = ZoneSerializer(source="zone", read_only=True)
    address_detail = AddressSerializer(source="address", read_only=True)

    is_cost_center = serializers.BooleanField(source="organization_unit.is_cost_center", read_only=True)
    is_profit_center = serializers.BooleanField(source="organization_unit.is_profit_center", read_only=True)
    is_inventory_storable = serializers.BooleanField(source="organization_unit.is_inventory_storable", read_only=True)
    is_asset_assignable = serializers.BooleanField(source="organization_unit.is_asset_assignable", read_only=True)
    effective_from = serializers.DateField(source="organization_unit.effective_from", read_only=True, allow_null=True)
    effective_to = serializers.DateField(source="organization_unit.effective_to", read_only=True, allow_null=True)
    created_by = serializers.CharField(source="organization_unit.created_by", read_only=True, allow_null=True)
    updated_by = serializers.CharField(source="organization_unit.updated_by", read_only=True, allow_null=True)

    class Meta:
        model = BranchProfile
        fields = [
            "id", "organization_unit", "branch_code", "branch_name", "legal_entity",
            "branch_type", "region", "region_detail", "zone", "zone_detail",
            "address", "address_detail", "latitude", "longitude",
            "is_head_office", "is_bank_branch", "is_active",
            "is_cost_center", "is_profit_center", "is_inventory_storable",
            "is_asset_assignable", "effective_from", "effective_to",
            "created_by", "updated_by", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "organization_unit", "created_at", "updated_at",
            "created_by", "updated_by", "is_cost_center", "is_profit_center",
            "is_inventory_storable", "is_asset_assignable", "effective_from", "effective_to",
        ]

    def validate(self, attrs):
        region = attrs.get("region", getattr(self.instance, "region", None))
        zone = attrs.get("zone", getattr(self.instance, "zone", None))
        address = attrs.get("address", getattr(self.instance, "address", None))
        if region and zone and zone.region_id != region.id:
            raise serializers.ValidationError({"zone": "Selected zone does not belong to selected region."})
        if address and region and address.region_id != region.id:
            raise serializers.ValidationError({"address": "Selected address does not belong to selected region."})
        if address and zone and address.zone_id != zone.id:
            raise serializers.ValidationError({"address": "Selected address does not belong to selected zone."})
        return attrs

class DepartmentProfileSerializer(serializers.ModelSerializer):
    class Meta: model = DepartmentProfile; fields = "__all__"
class StrategicBusinessUnitProfileSerializer(serializers.ModelSerializer):
    class Meta: model = StrategicBusinessUnitProfile; fields = "__all__"
class CostCenterProfileSerializer(serializers.ModelSerializer):
    class Meta: model = CostCenterProfile; fields = "__all__"
class ProfitCenterProfileSerializer(serializers.ModelSerializer):
    class Meta: model = ProfitCenterProfile; fields = "__all__"
class PhysicalLocationProfileSerializer(serializers.ModelSerializer):
    class Meta: model = PhysicalLocationProfile; fields = "__all__"
class CustodianAssignmentSerializer(serializers.ModelSerializer):
    class Meta: model = CustodianAssignment; fields = "__all__"
class OrganizationRelationshipSerializer(serializers.ModelSerializer):
    class Meta: model = OrganizationRelationship; fields = "__all__"
