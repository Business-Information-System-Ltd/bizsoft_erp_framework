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
Provides legal entity domain validations.
"""

from erp_organization.validators.organization_validator import BusinessValidationError, PermissionDeniedError, OrganizationValidator
from erp_organization.domain_policies.base import BaseOrganizationDomainPolicyService

class LegalEntityDomainPolicyService(BaseOrganizationDomainPolicyService):
    @staticmethod
    def validate_legal_entity_data(data): OrganizationValidator.require(data.get('country_code'),'country_code'); OrganizationValidator.require(data.get('functional_currency_code'),'functional_currency_code'); return True
    @staticmethod
    def validate_financial_year_start(month,day): return OrganizationValidator.validate_financial_year_start(month,day)
    @staticmethod
    def validate_can_use_legal_entity(legal_entity): return LegalEntityDomainPolicyService.validate_active(legal_entity.organization_unit if hasattr(legal_entity,'organization_unit') else legal_entity)
