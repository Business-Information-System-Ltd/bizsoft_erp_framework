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
Provides relationship domain validations.
"""

from erp_organization.validators.organization_validator import BusinessValidationError, PermissionDeniedError, OrganizationValidator
class OrganizationRelationshipDomainPolicyService:
    @staticmethod
    def validate_relationship_data(data):
        if data.get('from_unit') == data.get('to_unit'): raise BusinessValidationError('Relationship cannot link a unit to itself.')
        return True
    @staticmethod
    def validate_no_self_relationship(from_unit,to_unit):
        if from_unit and to_unit and from_unit.id==to_unit.id: raise BusinessValidationError('Relationship cannot link a unit to itself.')
        return True
    @staticmethod
    def validate_relationship_allowed(from_unit,to_unit,relationship_type): return OrganizationRelationshipDomainPolicyService.validate_no_self_relationship(from_unit,to_unit)
