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
Provides persistence helper for legal_entity.
"""

from erp_organization.repositories.organization_unit_repository import OrganizationUnitRepository
from django.db.models import Q
from erp_organization.models import LegalEntityProfile

class LegalEntityRepository(OrganizationUnitRepository):
    def get_filtered_legal_entities(
            self,
            filters
        ):
    
            queryset = LegalEntityProfile.objects.all()
    
            is_active = filters.get("is_active")
            legal_entity_code = filters.get("legal_entity_code")
            legal_entity_name = filters.get("legal_entity_name")
            legal_form = filters.get("legal_form")
            registration_no = filters.get("registration_no")
            tax_registration_no = filters.get("tax_registration_no")
            country_code = filters.get("country_code")
            functional_currency_code = filters.get("functional_currency_code")
            presentation_currency_code = filters.get("presentation_currency_code")
            financial_year_start_month = filters.get("financial_year_start_month")
            financial_year_start_day = filters.get("financial_year_start_day")
            search = filters.get("search")
    
            
            if is_active:
                if is_active.upper() == "ACTIVE":
                    queryset = queryset.filter(is_active=True)
                elif is_active.upper() == "INACTIVE":
                    queryset = queryset.filter(is_active=False)
    
            
            if legal_entity_code:
                queryset = queryset.filter(
                    legal_entity_code=legal_entity_code
                )
    
            if legal_entity_name:
                queryset = queryset.filter(
                    legal_entity_name=legal_entity_name
                )

            if country_code:  
                queryset = queryset.filter(
                    country_code=country_code
                )

            if legal_form:
                queryset = queryset.filter(
                    legal_form=legal_form
                )
            if registration_no:
                queryset = queryset.filter(
                    registration_no=registration_no
                )

            if tax_registration_no:
                queryset = queryset.filter(
                    tax_registration_no=tax_registration_no
                )

            if functional_currency_code:
                queryset = queryset.filter(
                    functional_currency_code=functional_currency_code
                )

            if presentation_currency_code:
                queryset = queryset.filter(
                    presentation_currency_code=presentation_currency_code
                )
    
            if financial_year_start_month:
                queryset = queryset.filter(
                    financial_year_start_month=financial_year_start_month
                )
            
            if financial_year_start_day:
                queryset = queryset.filter(
                    financial_year_start_day=financial_year_start_day
                )
    
            
            if search:
                queryset = queryset.filter(
                    Q(legal_entity_code__icontains=search) |
                    Q(legal_entity_name__icontains=search) |
                    Q(country_code__icontains=search) |
                    Q(legal_form__icontains=search) |
                    Q(registration_no__icontains=search) |
                    Q(tax_registration_no__icontains=search) |
                    Q(functional_currency_code__icontains=search) |
                    Q(presentation_currency_code__icontains=search) |
                    Q(financial_year_start_month__icontains=search) |
                    Q(financial_year_start_day__icontains=search) 
                )
                
    
            return queryset
    
