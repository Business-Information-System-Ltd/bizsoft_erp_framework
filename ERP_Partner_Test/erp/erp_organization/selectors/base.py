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
Provides base selector helpers for organization units.
"""


from erp_organization.models import OrganizationUnit

class BaseUnitSelector:
    unit_type=None
    @classmethod
    def queryset(cls):
        qs=OrganizationUnit.objects.all()
        return qs.filter(unit_type=cls.unit_type) if cls.unit_type else qs
    @classmethod
    def get_by_code(cls,code): return cls.queryset().filter(unit_code=code).first()
    @classmethod
    def get_active_by_code(cls,code): return cls.queryset().filter(unit_code=code,is_active=True).first()
    @classmethod
    def list_active(cls): return cls.queryset().filter(is_active=True).order_by('unit_code')
    @classmethod
    def exists(cls,code): return cls.queryset().filter(unit_code=code).exists()
