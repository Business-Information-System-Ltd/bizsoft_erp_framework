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
Provides shared validation helpers for organization data.
"""

try:
    from bizsoft.core.errors.exceptions import BusinessValidationError, NotFoundError, DuplicateRecordError, PermissionDeniedError, ConfigurationError, UnexpectedSystemError
except Exception:
    class BusinessValidationError(Exception): pass
    class NotFoundError(Exception): pass
    class DuplicateRecordError(Exception): pass
    class PermissionDeniedError(Exception): pass
    class ConfigurationError(Exception): pass
    class UnexpectedSystemError(Exception): pass


import re

class OrganizationValidator:
    CODE_PATTERN=re.compile(r'^[A-Z0-9_\-]+$')
    @staticmethod
    def require(value,field_name):
        if value in (None,''): raise BusinessValidationError(f'{field_name} is required.')
        return True
    @staticmethod
    def validate_code_format(code,field_name='code'):
        OrganizationValidator.require(code,field_name)
        if not OrganizationValidator.CODE_PATTERN.match(str(code)): raise BusinessValidationError(f'{field_name} must contain only uppercase letters, numbers, underscore, or hyphen.')
        return True
    @staticmethod
    def validate_effective_dates(effective_from,effective_to):
        if effective_from and effective_to and effective_from>effective_to: raise BusinessValidationError('effective_from must be before or equal to effective_to.')
        return True
    @staticmethod
    def validate_unit_type(unit,expected_type):
        if not unit or unit.unit_type!=expected_type: raise BusinessValidationError(f'Expected organization unit type {expected_type}.')
        return True
    @staticmethod
    def validate_no_self_parent(unit_id,parent_unit_id):
        if unit_id and parent_unit_id and unit_id==parent_unit_id: raise BusinessValidationError('A unit cannot be parent of itself.')
        return True
    @staticmethod
    def validate_financial_year_start(month,day):
        if int(month)<1 or int(month)>12: raise BusinessValidationError('Financial year month must be 1 to 12.')
        if int(day)<1 or int(day)>31: raise BusinessValidationError('Financial year day must be 1 to 31.')
        return True
    @staticmethod
    def validate_required_legal_entity(legal_entity):
        if not legal_entity: raise BusinessValidationError('Legal entity is required.')
        return True
    @staticmethod
    def validate_branch_belongs_to_legal_entity(branch,legal_entity):
        if branch and legal_entity and branch.legal_entity_id!=legal_entity.id: raise BusinessValidationError('Branch must belong to selected legal entity.')
        return True
    @staticmethod
    def validate_no_circular_hierarchy(unit,parent_unit):
        current=parent_unit
        while current:
            if unit and current.id==unit.id: raise BusinessValidationError('Circular organization hierarchy is not allowed.')
            current=current.parent_unit
        return True
    @staticmethod
    def validate_physical_location_responsibility(data):
        if data.get('is_asset_assignable') and not (data.get('responsible_branch') or data.get('responsible_department')):
            raise BusinessValidationError('Asset assignable location should have responsible branch or department.')
        return True
