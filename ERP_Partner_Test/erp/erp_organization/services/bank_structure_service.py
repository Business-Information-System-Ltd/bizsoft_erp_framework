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
Provides national-bank-friendly organization helpers.
"""


from erp_organization.constants import PhysicalLocationType
from erp_organization.models import BranchProfile, PhysicalLocationProfile
from erp_organization.services.branch_application_service import BranchApplicationService
from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService

class BankStructureService:
    @staticmethod
    def create_head_office(user,legal_entity_code,branch_data):
        data={**branch_data,'legal_entity_code':legal_entity_code,'is_head_office':True,'is_bank_branch':True}
        return BranchApplicationService.create_branch(user=user,data=data)
    @staticmethod
    def create_bank_branch(user,legal_entity_code,branch_data):
        data={**branch_data,'legal_entity_code':legal_entity_code,'is_bank_branch':True}
        return BranchApplicationService.create_branch(user=user,data=data)
    @staticmethod
    def create_atm_location(user,branch_code,location_data):
        data={**location_data,'responsible_branch_code':branch_code,'location_type':PhysicalLocationType.ATM_SITE,'is_internal':False,'is_asset_assignable':True}
        return PhysicalLocationApplicationService.create_physical_location(user=user,data=data)
    @staticmethod
    def create_data_center(user,legal_entity_code,location_data):
        data={**location_data,'location_type':PhysicalLocationType.DATA_CENTER,'is_asset_assignable':True}
        return PhysicalLocationApplicationService.create_physical_location(user=user,data=data)
    @staticmethod
    def create_dr_site(user,legal_entity_code,location_data):
        data={**location_data,'location_type':PhysicalLocationType.DR_SITE,'is_asset_assignable':True}
        return PhysicalLocationApplicationService.create_physical_location(user=user,data=data)
    @staticmethod
    def list_bank_branches(legal_entity_code=None):
        qs=BranchProfile.objects.filter(is_bank_branch=True,is_active=True)
        return qs.filter(legal_entity__unit_code=legal_entity_code) if legal_entity_code else qs
    @staticmethod
    def list_atm_locations(branch_code=None):
        qs=PhysicalLocationProfile.objects.filter(location_type=PhysicalLocationType.ATM_SITE,is_active=True)
        return qs.filter(responsible_branch__unit_code=branch_code) if branch_code else qs
    @staticmethod
    def list_branch_asset_locations(branch_code): return PhysicalLocationProfile.objects.filter(responsible_branch__unit_code=branch_code,is_asset_assignable=True,is_active=True)
    @staticmethod
    def list_branch_departments(branch_code): return []
