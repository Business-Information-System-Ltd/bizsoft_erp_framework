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
Provides persistence helper for physical locations.
"""

from erp_organization.repositories.organization_unit_repository import OrganizationUnitRepository
from django.db.models import Q
from erp_organization.models import PhysicalLocationProfile

class PhysicalLocationRepository(OrganizationUnitRepository):

    def get_filtered_physical_locations(
        self,
        filters
    ):

    

        queryset = PhysicalLocationProfile.objects.all()

        is_active = filters.get("is_active")
        location_code = filters.get("location_code")
        location_name = filters.get("location_name")
        location_type = filters.get("location_type")
        legal_entity = filters.get("legal_entity")
        responsible_department = filters.get("responsible_department")
        responsible_branch = filters.get("responsible_branch")
        search = filters.get("search")

        
        if is_active:
            if is_active.upper() == "ACTIVE":
                queryset = queryset.filter(is_active=True)
            elif is_active.upper() == "INACTIVE":
                queryset = queryset.filter(is_active=False)

        
        if location_code:
            queryset = queryset.filter(
                location_code=location_code
            )

        if location_name:
            queryset = queryset.filter(
                location_name=location_name
            )
        if location_type:
            queryset = queryset.filter(
                location_type=location_type
            )
        
        if legal_entity:
            queryset = queryset.filter(
                legal_entity_id=legal_entity
            )
        
        if responsible_department:
            queryset = queryset.filter(
                responsible_department_id=responsible_department
            )

        if responsible_branch:
            queryset = queryset.filter(
                responsible_branch_id=responsible_branch
            )

        
        if search:
            queryset = queryset.filter(
                Q(location_code__icontains=search) |
                Q(location_name__icontains=search) |
                Q(location_type__icontains=search) |
                Q(legal_entity__legal_entity_name__icontains=search) |
                Q(responsible_department__department_name__icontains=search) |
                Q(responsible_branch__branch_name__icontains=search)
            )
            

        return queryset
