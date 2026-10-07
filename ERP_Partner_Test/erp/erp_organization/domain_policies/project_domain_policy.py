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
Provides project date validations.
"""

from erp_organization.validators.organization_validator import BusinessValidationError, PermissionDeniedError, OrganizationValidator
class ProjectDomainPolicyService:
    @staticmethod
    def validate_project_dates(start_date,end_date):
        OrganizationValidator.require(start_date,'start_date')
        if end_date and end_date < start_date: raise BusinessValidationError('Project end date cannot be before start date.')
        return True
    @staticmethod
    def validate_project_can_be_used(project):
        if not project or not project.is_active: raise BusinessValidationError('Inactive project cannot be used.')
        return True
