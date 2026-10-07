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
Registers organization references with core_db when available.
"""


try:
    from core_db.registry import ReferenceRegistry
except Exception:
    ReferenceRegistry=None

class OrganizationReferenceRegistrationService:
    @staticmethod
    def _register(name,unit_type):
        if not ReferenceRegistry or not hasattr(ReferenceRegistry,'register'): return False
        ReferenceRegistry.register(name,{'table':'erp_organization_organizationunit','id_field':'id','code_field':'unit_code','name_field':'unit_name','active_field':'is_active','search_fields':['unit_code','unit_name'],'default_order_by':'unit_code','where_conditions':{'unit_type':unit_type}})
        return True
    @classmethod
    def register_legal_entity(cls): return cls._register('LEGAL_ENTITY','LEGAL_ENTITY')
    @classmethod
    def register_branch(cls): return cls._register('BRANCH','BRANCH')
    @classmethod
    def register_department(cls): return cls._register('DEPARTMENT','DEPARTMENT')
    @classmethod
    def register_cost_center(cls): return cls._register('COST_CENTER','COST_CENTER')
    @classmethod
    def register_profit_center(cls): return cls._register('PROFIT_CENTER','PROFIT_CENTER')
    @classmethod
    def register_physical_location(cls): return cls._register('PHYSICAL_LOCATION','PHYSICAL_LOCATION')
    @classmethod
    def register_all(cls):
        return [cls.register_legal_entity(),cls.register_branch(),cls.register_department(),cls.register_cost_center(),cls.register_profit_center(),cls.register_physical_location()]
