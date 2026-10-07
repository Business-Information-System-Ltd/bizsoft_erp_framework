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
Provides branch domain validations.
"""

from erp_organization.validators.organization_validator import BusinessValidationError, PermissionDeniedError, OrganizationValidator
from erp_organization.domain_policies.base import BaseOrganizationDomainPolicyService

class BranchDomainPolicyService(BaseOrganizationDomainPolicyService):
    @staticmethod
    def validate_branch_data(data): OrganizationValidator.validate_required_legal_entity(data.get('legal_entity')); return True
    @staticmethod
    def validate_can_use_branch(branch): return BranchDomainPolicyService.validate_active(branch.organization_unit if hasattr(branch,'organization_unit') else branch)
