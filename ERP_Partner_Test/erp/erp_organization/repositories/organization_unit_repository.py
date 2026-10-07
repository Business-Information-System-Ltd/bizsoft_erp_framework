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
Provides persistence helper for organization units.
"""


from django.db import IntegrityError
from erp_organization.models import OrganizationUnit
from erp_organization.validators.organization_validator import DuplicateRecordError

class OrganizationUnitRepository:
    def get_by_code(self,unit_code,unit_type=None):
        qs=OrganizationUnit.objects.filter(unit_code=unit_code)
        return qs.filter(unit_type=unit_type).first() if unit_type else qs.first()
    def get_active_by_code(self,unit_code,unit_type=None):
        qs=OrganizationUnit.objects.filter(unit_code=unit_code,is_active=True)
        return qs.filter(unit_type=unit_type).first() if unit_type else qs.first()
    def list_by_type(self,unit_type,legal_entity=None,is_active=True):
        qs=OrganizationUnit.objects.filter(unit_type=unit_type)
        if legal_entity: qs=qs.filter(legal_entity=legal_entity)
        if is_active is not None: qs=qs.filter(is_active=is_active)
        return qs.order_by('unit_code')
    def create_unit(self,data):
        try: return OrganizationUnit.objects.create(**data)
        except IntegrityError as exc: raise DuplicateRecordError('Duplicate organization unit code/type.') from exc
    def update_unit(self,unit_id,data):
        obj=OrganizationUnit.objects.get(id=unit_id)
        for k,v in data.items(): setattr(obj,k,v)
        obj.save(); return obj
    def deactivate_unit(self,unit_id):
        obj=OrganizationUnit.objects.get(id=unit_id); obj.is_active=False; obj.save(update_fields=['is_active','updated_at']); return obj
    def exists(self,unit_code,unit_type=None): return self.get_by_code(unit_code,unit_type) is not None
    def get_children(self,parent_unit): return OrganizationUnit.objects.filter(parent_unit=parent_unit,is_active=True).order_by('unit_code')
    def get_parent(self,unit): return unit.parent_unit
