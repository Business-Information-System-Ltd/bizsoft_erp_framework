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
Manages flexible organization relationships.
"""

from django.utils import timezone
from erp_organization.models import OrganizationRelationship
from erp_organization.domain_policies.relationship_domain_policy import OrganizationRelationshipDomainPolicyService

class OrganizationRelationshipService:
    @staticmethod
    def create_relationship(from_unit,to_unit,relationship_type,effective_from=None,effective_to=None):
        OrganizationRelationshipDomainPolicyService.validate_no_self_relationship(from_unit,to_unit)
        return OrganizationRelationship.objects.create(from_unit=from_unit,to_unit=to_unit,relationship_type=relationship_type,effective_from=effective_from,effective_to=effective_to)
    @staticmethod
    def deactivate_relationship(relationship_id):
        rel=OrganizationRelationship.objects.get(id=relationship_id); rel.is_active=False; rel.save(update_fields=['is_active','updated_at']); return rel
    @staticmethod
    def get_active_relationships(from_unit=None,to_unit=None,relationship_type=None,as_of_date=None):
        qs=OrganizationRelationship.objects.filter(is_active=True)
        if from_unit: qs=qs.filter(from_unit=from_unit)
        if to_unit: qs=qs.filter(to_unit=to_unit)
        if relationship_type: qs=qs.filter(relationship_type=relationship_type)
        return qs
    @staticmethod
    def get_units_related_to(unit,relationship_type): return [r.to_unit for r in OrganizationRelationshipService.get_active_relationships(from_unit=unit,relationship_type=relationship_type)]
