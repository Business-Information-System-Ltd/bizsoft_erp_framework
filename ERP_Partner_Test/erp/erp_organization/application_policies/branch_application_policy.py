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
Provides branch application policy checks.
"""

from erp_organization.application_policies.base import BaseOrganizationApplicationPolicyService
from erp_organization.domain_policies.branch_domain_policy import BranchDomainPolicyService

class BranchApplicationPolicyService(BaseOrganizationApplicationPolicyService):
    @staticmethod
    def validate_create_branch_allowed(user, legal_entity_code=None): return True
    @staticmethod
    def validate_can_use_branch(branch): return BranchDomainPolicyService.validate_can_use_branch(branch)
