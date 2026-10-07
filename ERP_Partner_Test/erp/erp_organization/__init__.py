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
Exposes package metadata and lazy service exports.
"""

__version__ = "1.0.0"
__author__ = "Business Information Systems Ltd. / BizSoft"
__package_name__ = "erp_organization"


def __getattr__(name):
    if name == "OrganizationHierarchyService":
        from .services.hierarchy_service import OrganizationHierarchyService
        return OrganizationHierarchyService
    if name == "OrganizationReferenceRegistrationService":
        from .services.reference_registration_service import OrganizationReferenceRegistrationService
        return OrganizationReferenceRegistrationService
    if name == "BankStructureService":
        from .services.bank_structure_service import BankStructureService
        return BankStructureService
    raise AttributeError(name)


__all__ = ["OrganizationHierarchyService", "OrganizationReferenceRegistrationService", "BankStructureService"]
