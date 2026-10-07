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
Provides read-side selector for BranchSelector.
"""

from erp_organization.constants import OrganizationUnitType
from erp_organization.selectors.base import BaseUnitSelector

class BranchSelector(BaseUnitSelector):
    unit_type=OrganizationUnitType.BRANCH

    @classmethod
    def list_by_legal_entity(cls, legal_entity): return cls.queryset().filter(legal_entity=legal_entity,is_active=True).order_by('unit_code')
