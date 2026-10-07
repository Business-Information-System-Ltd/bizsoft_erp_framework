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
Provides persistence helper for department.
"""

from erp_organization.repositories.organization_unit_repository import OrganizationUnitRepository
from django.db.models import Q
from erp_organization.models import DepartmentProfile


class DepartmentRepository(OrganizationUnitRepository):
    def get_filtered_departments(
            self,
            filters
        ):
    
            queryset = DepartmentProfile.objects.all()
    
            is_active = filters.get("is_active")
            department_code = filters.get("department_code")
            department_name = filters.get("department_name")
            legal_entity = filters.get("legal_entity")
            branch = filters.get("branch")
            parent_department = filters.get("parent_department")
            search = filters.get("search")
    
            
            if is_active:
                if is_active.upper() == "ACTIVE":
                    queryset = queryset.filter(is_active=True)
                elif is_active.upper() == "INACTIVE":
                    queryset = queryset.filter(is_active=False)
    
            
            if department_code:
                queryset = queryset.filter(
                    department_code=department_code
                )

            if department_name:
                queryset = queryset.filter(
                    department_name__icontains=department_name
                )

            if branch:
                queryset = queryset.filter(
                    branch_id=branch
                )

            if parent_department:
                queryset = queryset.filter(
                    parent_department_id=parent_department
                )

            if legal_entity:
                queryset = queryset.filter(
                    legal_entity_id=legal_entity
                )
    
            
            if search:
                queryset = queryset.filter(
                    Q(department_code__icontains=search) |
                    Q(department_name__icontains=search) 
                )
                
    
            return queryset
    
