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
Provides organization tree and descendant helpers.
"""

from erp_organization.models import OrganizationUnit

class OrganizationHierarchyService:
    @staticmethod
    def get_children(unit): return OrganizationUnit.objects.filter(parent_unit=unit,is_active=True).order_by('unit_code')
    @staticmethod
    def get_descendants(unit):
        result=[]
        for child in OrganizationHierarchyService.get_children(unit):
            result.append(child); result.extend(OrganizationHierarchyService.get_descendants(child))
        return result
    @staticmethod
    def get_tree(unit_type=None):
        qs=OrganizationUnit.objects.filter(parent_unit__isnull=True,is_active=True)
        if unit_type: qs=qs.filter(unit_type=unit_type)
        def node(u): return {'id':u.id,'code':u.unit_code,'name':u.unit_name,'type':u.unit_type,'children':[node(c) for c in OrganizationHierarchyService.get_children(u)]}
        return [node(u) for u in qs.order_by('unit_code')]
