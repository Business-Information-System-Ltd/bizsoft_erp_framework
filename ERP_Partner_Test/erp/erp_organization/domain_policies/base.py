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
Provides reusable domain policy checks.
"""

from erp_organization.validators.organization_validator import BusinessValidationError, PermissionDeniedError, OrganizationValidator

class BaseOrganizationDomainPolicyService:
    @staticmethod
    def validate_active(unit):
        if not unit or not getattr(unit,'is_active',False): raise BusinessValidationError('Inactive organization unit cannot be used.')
        return True
    @staticmethod
    def validate_effective_dates(effective_from,effective_to): return OrganizationValidator.validate_effective_dates(effective_from,effective_to)
    @staticmethod
    def validate_no_self_parent(unit_id,parent_unit_id): return OrganizationValidator.validate_no_self_parent(unit_id,parent_unit_id)
