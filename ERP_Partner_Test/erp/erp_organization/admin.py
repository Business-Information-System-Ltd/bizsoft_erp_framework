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
Registers organization models in Django admin.
"""


from django.contrib import admin
from erp_organization.models import *

@admin.register(OrganizationUnit)
class OrganizationUnitAdmin(admin.ModelAdmin):
    list_display=('unit_code','unit_name','unit_type','legal_entity','parent_unit','is_cost_center','is_profit_center','is_inventory_storable','is_asset_assignable','is_active')
    search_fields=('unit_code','unit_name')
    list_filter=('unit_type','status','is_active','is_cost_center','is_profit_center','is_inventory_storable','is_asset_assignable')

@admin.register(LegalEntityProfile)
class LegalEntityProfileAdmin(admin.ModelAdmin):
    list_display=('legal_entity_code','legal_entity_name','country_code','functional_currency_code','is_active')
    search_fields=('legal_entity_code','legal_entity_name')
    list_filter=('country_code','is_active')

@admin.register(BranchProfile)
class BranchProfileAdmin(admin.ModelAdmin):
    list_display=('branch_code','branch_name','legal_entity','region','zone','is_head_office','is_bank_branch','is_active')
    search_fields=('branch_code','branch_name')
    list_filter=('is_head_office','is_bank_branch','is_active')

@admin.register(DepartmentProfile)
class DepartmentProfileAdmin(admin.ModelAdmin):
    list_display=('department_code','department_name','legal_entity','branch','parent_department','is_active')
    search_fields=('department_code','department_name')
    list_filter=('is_active',)

@admin.register(PhysicalLocationProfile)
class PhysicalLocationProfileAdmin(admin.ModelAdmin):
    list_display=('location_code','location_name','location_type','responsible_branch','responsible_department','is_internal','is_asset_assignable','is_active')
    search_fields=('location_code','location_name')
    list_filter=('location_type','is_internal','is_asset_assignable','is_active')

for model in [EnterpriseGroupProfile,StrategicBusinessUnitProfile,SBUEntityAssignment,FacilityProfile,WarehouseProfile,StorageLocationProfile,ProcessProfile,WorkstationProfile,ProjectProfile,ProjectSiteProfile,CostCenterProfile,ProfitCenterProfile,CustodianAssignment,OrganizationRelationship]:
    try: admin.site.register(model)
    except admin.sites.AlreadyRegistered: pass
