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
# Defines Django ORM models for ERP organization master data.
# """


# from django.db import models
# from erp_organization.constants import CustodianType, OrganizationRelationshipType, OrganizationUnitType, PhysicalLocationType, UnitStatus

# class OrganizationUnit(models.Model):
#     unit_code=models.CharField(max_length=50,db_index=True)
#     unit_name=models.CharField(max_length=255)
#     unit_type=models.CharField(max_length=50,choices=OrganizationUnitType.CHOICES,db_index=True)
#     legal_entity=models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT,related_name='legal_entity_units')
#     parent_unit=models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT,related_name='child_units')
#     status=models.CharField(max_length=30,choices=UnitStatus.CHOICES,default=UnitStatus.ACTIVE)
#     is_cost_center=models.BooleanField(default=False)
#     is_profit_center=models.BooleanField(default=False)
#     is_inventory_storable=models.BooleanField(default=False)
#     is_asset_assignable=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=True)
#     effective_from=models.DateField(null=True,blank=True)
#     effective_to=models.DateField(null=True,blank=True)
#     created_by=models.CharField(max_length=100,null=True,blank=True)
#     updated_by=models.CharField(max_length=100,null=True,blank=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     class Meta:
#         ordering=['unit_type','unit_code']
#         constraints=[models.UniqueConstraint(fields=['unit_code','unit_type'],name='erp_org_unit_unique_code_type')]
#         indexes=[models.Index(fields=['unit_code']),models.Index(fields=['unit_type']),models.Index(fields=['legal_entity']),models.Index(fields=['parent_unit']),models.Index(fields=['is_active'])]
#     def __str__(self): return f'{self.unit_code} - {self.unit_name}'

# class EnterpriseGroupProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='enterprise_group_profile')
#     group_code=models.CharField(max_length=50,unique=True)
#     group_name=models.CharField(max_length=255)
#     parent_country_code=models.CharField(max_length=10,blank=True)
#     reporting_currency_code=models.CharField(max_length=10,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self): return self.group_code

# class LegalEntityProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='legal_entity_profile')
#     legal_entity_code=models.CharField(max_length=50,unique=True,db_index=True)
#     legal_entity_name=models.CharField(max_length=255)
#     legal_name=models.CharField(max_length=255,blank=True)
#     registration_no=models.CharField(max_length=100,blank=True)
#     tax_registration_no=models.CharField(max_length=100,blank=True)
#     country_code=models.CharField(max_length=10)
#     functional_currency_code=models.CharField(max_length=10)
#     presentation_currency_code=models.CharField(max_length=10,blank=True)
#     financial_year_start_month=models.PositiveSmallIntegerField(default=4)
#     financial_year_start_day=models.PositiveSmallIntegerField(default=1)
#     parent_group=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='legal_entities_in_group')
#     legal_form=models.CharField(max_length=100,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self): return self.legal_entity_code

# class BranchProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='branch_profile')
#     branch_code=models.CharField(max_length=50,unique=True,db_index=True)
#     branch_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='branch_profiles')
#     branch_type=models.CharField(max_length=50,blank=True)
#     branch_manager_id=models.CharField(max_length=100,null=True,blank=True)
#     region_code=models.CharField(max_length=50,null=True,blank=True)
#     zone_code=models.CharField(max_length=50,null=True,blank=True)
#     is_head_office=models.BooleanField(default=False)
#     is_bank_branch=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self): return self.branch_code

# class DepartmentProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='department_profile')
#     department_code=models.CharField(max_length=50,unique=True,db_index=True)
#     department_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='department_profiles')
#     branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_departments')
#     parent_department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='sub_department_profiles')
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self): return self.department_code

# class StrategicBusinessUnitProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_profile')
#     sbu_code=models.CharField(max_length=50,unique=True,db_index=True)
#     sbu_name=models.CharField(max_length=255)
#     sbu_type=models.CharField(max_length=50,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     def __str__(self): return self.sbu_code

# class SBUEntityAssignment(models.Model):
#     sbu=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_entity_assignments')
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_assignments')
#     effective_from=models.DateField(null=True,blank=True)
#     effective_to=models.DateField(null=True,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class FacilityProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='facility_profile')
#     facility_code=models.CharField(max_length=50,unique=True,db_index=True)
#     facility_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='facility_profiles')
#     branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_facilities')
#     facility_type=models.CharField(max_length=50,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class WarehouseProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='warehouse_profile')
#     warehouse_code=models.CharField(max_length=50,unique=True,db_index=True)
#     warehouse_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='warehouse_profiles')
#     branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_warehouses')
#     facility=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='facility_warehouses')
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class StorageLocationProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='storage_location_profile')
#     storage_location_code=models.CharField(max_length=50,unique=True,db_index=True)
#     storage_location_name=models.CharField(max_length=255)
#     warehouse=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='storage_locations')
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class ProcessProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='process_profile')
#     process_code=models.CharField(max_length=50,unique=True); process_name=models.CharField(max_length=255)
#     is_active=models.BooleanField(default=True)

# class WorkstationProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='workstation_profile')
#     workstation_code=models.CharField(max_length=50,unique=True); workstation_name=models.CharField(max_length=255)
#     process=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='workstations')
#     is_active=models.BooleanField(default=True)

# class ProjectProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='project_profile')
#     project_code=models.CharField(max_length=50,unique=True,db_index=True)
#     project_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='project_profiles')
#     start_date=models.DateField()
#     end_date=models.DateField(null=True,blank=True)
#     project_manager_id=models.CharField(max_length=100,null=True,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class ProjectSiteProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='project_site_profile')
#     site_code=models.CharField(max_length=50,unique=True); site_name=models.CharField(max_length=255)
#     project=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='project_sites')
#     is_active=models.BooleanField(default=True)

# class CostCenterProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='cost_center_profile')
#     cost_center_code=models.CharField(max_length=50,unique=True,db_index=True)
#     cost_center_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='cost_center_profiles')
#     branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_cost_centers')
#     department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='department_cost_centers')
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class ProfitCenterProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='profit_center_profile')
#     profit_center_code=models.CharField(max_length=50,unique=True,db_index=True)
#     profit_center_name=models.CharField(max_length=255)
#     legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='profit_center_profiles')
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class PhysicalLocationProfile(models.Model):
#     organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='physical_location_profile')
#     location_code=models.CharField(max_length=50,unique=True,db_index=True)
#     location_name=models.CharField(max_length=255)
#     location_type=models.CharField(max_length=50,choices=PhysicalLocationType.CHOICES,default=PhysicalLocationType.OTHER)
#     legal_entity=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='physical_location_profiles')
#     responsible_branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='responsible_locations')
#     responsible_department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='department_locations')
#     address=models.TextField(blank=True)
#     is_internal=models.BooleanField(default=True)
#     is_asset_assignable=models.BooleanField(default=False)
#     is_inventory_storable=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class CustodianAssignment(models.Model):
#     custodian_code=models.CharField(max_length=50,db_index=True)
#     custodian_name=models.CharField(max_length=255)
#     custodian_type=models.CharField(max_length=30,choices=CustodianType.CHOICES,default=CustodianType.EMPLOYEE)
#     legal_entity=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='custodians')
#     branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_custodians')
#     department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='department_custodians')
#     employee_id=models.CharField(max_length=100,null=True,blank=True)
#     effective_from=models.DateField(null=True,blank=True)
#     effective_to=models.DateField(null=True,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

# class OrganizationRelationship(models.Model):
#     from_unit=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='relationships_from')
#     to_unit=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='relationships_to')
#     relationship_type=models.CharField(max_length=50,choices=OrganizationRelationshipType.CHOICES)
#     effective_from=models.DateField(null=True,blank=True)
#     effective_to=models.DateField(null=True,blank=True)
#     is_active=models.BooleanField(default=True)
#     created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
#     class Meta:
#         indexes=[models.Index(fields=['from_unit']),models.Index(fields=['to_unit']),models.Index(fields=['relationship_type']),models.Index(fields=['is_active'])]
#     def __str__(self): return f'{self.from_unit} {self.relationship_type} {self.to_unit}'


"""
BizSoft ERP - ERP Organization

Company: Business Information Systems Ltd. / BizSoft
Author: Business Information Systems Ltd. / BizSoft
Package: erp_organization
Version: 1.0.0

Purpose:
This file is part of the erp_organization ERP business foundation package.

Important:
- This package defines legal entities, branches, departments, SBUs, facilities,
  warehouses, projects, cost centers, profit centers, physical locations,
  custodians, and flexible organization relationships.
- Organization tells where and who.
- Dimension tells how to classify, summarize, analyze, and report.
- Do not implement accounting posting, inventory movement, FAR depreciation,
  payroll, workflow routing, permission engine, audit trail, or notifications.
- core_* packages must not depend on erp_organization.

Rule:
Selectors read data.
Domain Policies validate domain truth.
Application Policies validate whether an action is allowed in context.
Application Services orchestrate use cases.

File Purpose:
Defines Django ORM models for ERP organization master data.
"""


from django.db import models
from erp_organization.constants import CustodianType, OrganizationRelationshipType, OrganizationUnitType, PhysicalLocationType, UnitStatus
from bizsoft.core.errors import ValidationERPError
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from zoneinfo import ZoneInfo
from datetime import datetime

class OrganizationUnit(models.Model):
    unit_code=models.CharField(max_length=50,db_index=True)
    unit_name=models.CharField(max_length=255)
    unit_type=models.CharField(max_length=50,choices=OrganizationUnitType.CHOICES,db_index=True)
    legal_entity=models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT,related_name='legal_entity_units')
    parent_unit=models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT,related_name='child_units')
    status=models.CharField(max_length=30,choices=UnitStatus.CHOICES,default=UnitStatus.ACTIVE)
    is_cost_center=models.BooleanField(default=False)
    is_profit_center=models.BooleanField(default=False)
    is_inventory_storable=models.BooleanField(default=False)
    is_asset_assignable=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    effective_from=models.DateField(null=True,blank=True)
    effective_to=models.DateField(null=True,blank=True)
    created_by=models.CharField(max_length=100,null=True,blank=True)
    updated_by=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['unit_type','unit_code']
        constraints=[models.UniqueConstraint(fields=['unit_code','unit_type'],name='erp_org_unit_unique_code_type')]
        indexes=[models.Index(fields=['unit_code']),models.Index(fields=['unit_type']),models.Index(fields=['legal_entity']),models.Index(fields=['parent_unit']),models.Index(fields=['is_active'])]
    def __str__(self): return f'{self.unit_code} - {self.unit_name}'

class EnterpriseGroupProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='enterprise_group_profile')
    group_code=models.CharField(max_length=50,unique=True)
    group_name=models.CharField(max_length=255)
    parent_country_code=models.CharField(max_length=10,blank=True)
    reporting_currency_code=models.CharField(max_length=10,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.group_code

class LegalEntityProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='legal_entity_profile')
    legal_entity_code=models.CharField(max_length=50,unique=True,db_index=True)
    legal_entity_name=models.CharField(max_length=255)
    legal_name=models.CharField(max_length=255,blank=True)
    registration_no=models.CharField(max_length=100,blank=True)
    tax_registration_no=models.CharField(max_length=100,blank=True)
    country_code=models.CharField(max_length=10)
    functional_currency_code=models.CharField(max_length=10)
    presentation_currency_code=models.CharField(max_length=10,blank=True)
    financial_year_start_month=models.PositiveSmallIntegerField(default=4)
    financial_year_start_day=models.PositiveSmallIntegerField(default=1)
    parent_group=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='legal_entities_in_group')
    legal_form=models.CharField(max_length=100,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.legal_entity_code


class Region(models.Model):
    region_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )

    region_name = models.CharField(
        max_length=255,
    )

    
    timezone_name = models.CharField(
        max_length=100,
        # default="Asia/Yangon",
        db_index=True,
        null=True,
        blank=True,
    )
    map_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "erp_organization_region"
        ordering = ["region_name"]

        indexes = [
            models.Index(
                fields=["region_code"],
            ),
            models.Index(
                fields=["is_active"],
            ),
            models.Index(
                fields=["timezone_name"],
            ),
        ]

    def __str__(self):
        return f"{self.region_name} ({self.timezone_name})"

TIMEZONE_ABBREVIATIONS = {
    "Asia/Yangon": "MMT",
    "Asia/Bangkok": "ICT",
    "Asia/Tokyo": "JST",
    "Asia/Kolkata": "IST",
    "Asia/Singapore": "SGT",
    "Asia/Kuala_Lumpur": "MYT",
    "Asia/Manila": "PHT",
    "Asia/Jakarta": "WIB",
    "Asia/Ho_Chi_Minh": "ICT",
    "Asia/Seoul": "KST",
    "Asia/Shanghai": "CST",
}
class Zone(models.Model):

    zone_code = models.CharField(
        max_length=50,
    )

    zone_name = models.CharField(
        max_length=100,
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="zones",
    )

    timezone_abbreviation = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    utc_offset = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def save(self, *args, **kwargs):

        if self.region_id:

            timezone_name = (
                self.region.timezone_name
            )

            if timezone_name:

                tz = ZoneInfo(
                    timezone_name
                )

                now = datetime.now(tz)

                self.timezone_abbreviation = (
                TIMEZONE_ABBREVIATIONS.get(
                    timezone_name,
                    now.tzname(),
                )
            )
                offset = now.utcoffset()

                if offset is not None:
                    total_seconds = int(
                        offset.total_seconds()
                    )

                    sign = (
                        "+"
                        if total_seconds >= 0
                        else "-"
                    )

                    total_seconds = abs(
                        total_seconds
                    )

                    hours = (
                        total_seconds // 3600
                    )

                    minutes = (
                        (total_seconds % 3600)
                        // 60
                    )

                    self.utc_offset = (
                        f"{sign}"
                        f"{hours:02d}:"
                        f"{minutes:02d}"
                    )

        super().save(
            *args,
            **kwargs,
        )

class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    township = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="addresses",
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.PROTECT,
        related_name="addresses",
    )
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    # country_code = models.CharField(max_length=3, default="MMR")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "erp_organization_address"
        ordering = ["city", "township", "address_line_1"]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["zone"]),
            models.Index(fields=["city"]),
            models.Index(fields=["township"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.address_line_1}, {self.township}, {self.city}"

    def clean(self):
        super().clean()
        if self.region_id and self.zone_id:
            if self.zone.region_id != self.region_id:
                raise ValidationERPError({
                    "zone": "Selected zone does not belong to selected region."
                })
        if self.region_id and not self.region.is_active:
            raise ValidationERPError({"region": "Selected region is inactive."})
        if self.zone_id and not self.zone.is_active:
            raise ValidationERPError({"zone": "Selected zone is inactive."})


class BranchProfile(models.Model):
    organization_unit = models.OneToOneField(
        OrganizationUnit,
        on_delete=models.CASCADE,
        related_name="branch_profile",
    )
    branch_code = models.CharField(max_length=50, unique=True, db_index=True)
    branch_name = models.CharField(max_length=255)
    legal_entity = models.ForeignKey(
        LegalEntityProfile,
        on_delete=models.PROTECT,
        related_name="branch_profiles",
    )
    branch_type = models.CharField(max_length=50, blank=True)

    
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="branches",
        null=True,
        blank=True,
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.PROTECT,
        related_name="branches",
        null=True,
        blank=True,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="branches",
        null=True,
        blank=True,
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    is_head_office = models.BooleanField(default=False)
    is_bank_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["branch_code"]
        indexes = [
            models.Index(fields=["branch_code"]),
            models.Index(fields=["region"]),
            models.Index(fields=["zone"]),
            models.Index(fields=["address"]),
            models.Index(fields=["legal_entity"]),
            models.Index(fields=["is_active"]),
        ]

    def clean(self):
        super().clean()

    
        if (
            self.region_id
            and self.zone_id
            and self.zone.region_id != self.region_id
        ):
            raise ValidationERPError(
                {
                    "zone": (
                        "Selected zone does not belong "
                        "to selected region."
                    )
                }
            )

    
        if (
            self.address_id
            and self.region_id
            and self.address.region_id != self.region_id
        ):
            raise ValidationERPError(
                {
                    "address": (
                        "Address region must match "
                        "branch region."
                    )
                }
            )

        if (
            self.address_id
            and self.zone_id
            and self.address.zone_id != self.zone_id
        ):
            raise ValidationERPError(
                {
                    "address": (
                        "Address zone must match "
                        "branch zone."
                    )
                }
            )

    def __str__(self):
        return self.branch_code

class DepartmentProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='department_profile')
    department_code=models.CharField(max_length=50,unique=True,db_index=True)
    department_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(LegalEntityProfile,on_delete=models.PROTECT,related_name='department_profiles')
    branch=models.ForeignKey(BranchProfile,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_departments')
    parent_department=models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT,related_name='sub_department_profiles')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.department_code

class StrategicBusinessUnitProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_profile')
    sbu_code=models.CharField(max_length=50,unique=True,db_index=True)
    sbu_name=models.CharField(max_length=255)
    sbu_type=models.CharField(max_length=50,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.sbu_code

class SBUEntityAssignment(models.Model):
    sbu=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_entity_assignments')
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='sbu_assignments')
    effective_from=models.DateField(null=True,blank=True)
    effective_to=models.DateField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class FacilityProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='facility_profile')
    facility_code=models.CharField(max_length=50,unique=True,db_index=True)
    facility_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='facility_profiles')
    branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_facilities')
    facility_type=models.CharField(max_length=50,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class WarehouseProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='warehouse_profile')
    warehouse_code=models.CharField(max_length=50,unique=True,db_index=True)
    warehouse_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='warehouse_profiles')
    branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_warehouses')
    facility=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='facility_warehouses')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class StorageLocationProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='storage_location_profile')
    storage_location_code=models.CharField(max_length=50,unique=True,db_index=True)
    storage_location_name=models.CharField(max_length=255)
    warehouse=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='storage_locations')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class ProcessProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='process_profile')
    process_code=models.CharField(max_length=50,unique=True); process_name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)

class WorkstationProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='workstation_profile')
    workstation_code=models.CharField(max_length=50,unique=True); workstation_name=models.CharField(max_length=255)
    process=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='workstations')
    is_active=models.BooleanField(default=True)

class ProjectProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='project_profile')
    project_code=models.CharField(max_length=50,unique=True,db_index=True)
    project_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='project_profiles')
    start_date=models.DateField()
    end_date=models.DateField(null=True,blank=True)
    project_manager_id=models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class ProjectSiteProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='project_site_profile')
    site_code=models.CharField(max_length=50,unique=True); site_name=models.CharField(max_length=255)
    project=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='project_sites')
    is_active=models.BooleanField(default=True)

class CostCenterProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='cost_center_profile')
    cost_center_code=models.CharField(max_length=50,unique=True,db_index=True)
    cost_center_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='cost_center_profiles')
    branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_cost_centers')
    department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='department_cost_centers')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class ProfitCenterProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='profit_center_profile')
    profit_center_code=models.CharField(max_length=50,unique=True,db_index=True)
    profit_center_name=models.CharField(max_length=255)
    legal_entity=models.ForeignKey(OrganizationUnit,on_delete=models.PROTECT,related_name='profit_center_profiles')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class PhysicalLocationProfile(models.Model):
    organization_unit=models.OneToOneField(OrganizationUnit,on_delete=models.CASCADE,related_name='physical_location_profile')
    location_code=models.CharField(max_length=50,unique=True,db_index=True)
    location_name=models.CharField(max_length=255)
    location_type=models.CharField(max_length=50,choices=PhysicalLocationType.CHOICES,default=PhysicalLocationType.OTHER)
    legal_entity=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='physical_location_profiles')
    responsible_branch=models.ForeignKey(BranchProfile,null=True,blank=True,on_delete=models.PROTECT,related_name='responsible_locations')
    responsible_department=models.ForeignKey(DepartmentProfile,null=True,blank=True,on_delete=models.PROTECT,related_name='department_locations')
    address=models.TextField(blank=True)
    is_internal=models.BooleanField(default=True)
    is_asset_assignable=models.BooleanField(default=False)
    is_inventory_storable=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class CustodianAssignment(models.Model):
    custodian_code=models.CharField(max_length=50,db_index=True)
    custodian_name=models.CharField(max_length=255)
    custodian_type=models.CharField(max_length=30,choices=CustodianType.CHOICES,default=CustodianType.EMPLOYEE)
    legal_entity=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='custodians')
    branch=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='branch_custodians')
    department=models.ForeignKey(OrganizationUnit,null=True,blank=True,on_delete=models.PROTECT,related_name='department_custodians')
    employee_id=models.CharField(max_length=100,null=True,blank=True)
    effective_from=models.DateField(null=True,blank=True)
    effective_to=models.DateField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class OrganizationRelationship(models.Model):
    from_unit=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='relationships_from')
    to_unit=models.ForeignKey(OrganizationUnit,on_delete=models.CASCADE,related_name='relationships_to')
    relationship_type=models.CharField(max_length=50,choices=OrganizationRelationshipType.CHOICES)
    effective_from=models.DateField(null=True,blank=True)
    effective_to=models.DateField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        indexes=[models.Index(fields=['from_unit']),models.Index(fields=['to_unit']),models.Index(fields=['relationship_type']),models.Index(fields=['is_active'])]
    def __str__(self): return f'{self.from_unit} {self.relationship_type} {self.to_unit}'

