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
Orchestrates legal entity creation.
"""

from django.db import transaction
from erp_organization.constants import OrganizationUnitType, PhysicalLocationType
from erp_organization.models import *
from erp_organization.validators.organization_validator import BusinessValidationError, NotFoundError, OrganizationValidator
from erp_organization.repositories.legal_entity_repository import LegalEntityRepository

class LegalEntityApplicationService:
    # @staticmethod
    # @transaction.atomic
    # def create_legal_entity(user=None,data=None):
    #     data=data or {}; OrganizationValidator.validate_code_format(data.get('legal_entity_code'),'legal_entity_code')
    #     OrganizationValidator.require(data.get('country_code'),'country_code'); OrganizationValidator.require(data.get('functional_currency_code'),'functional_currency_code')
    #     unit=OrganizationUnit.objects.create(unit_code=data['legal_entity_code'],unit_name=data.get('legal_entity_name',data['legal_entity_code']),unit_type=OrganizationUnitType.LEGAL_ENTITY,created_by=getattr(user,'username',None))
    #     return LegalEntityProfile.objects.create(organization_unit=unit,legal_entity_code=data['legal_entity_code'],legal_entity_name=data.get('legal_entity_name',data['legal_entity_code']),legal_name=data.get('legal_name',''),registration_no=data.get('registration_no',''),tax_registration_no=data.get('tax_registration_no',''),country_code=data['country_code'],functional_currency_code=data['functional_currency_code'],presentation_currency_code=data.get('presentation_currency_code',''),financial_year_start_month=data.get('financial_year_start_month',4),financial_year_start_day=data.get('financial_year_start_day',1),legal_form=data.get('legal_form',''))

    
    repository = LegalEntityRepository()
    @classmethod
    def get_filtered_legal_entities(
        cls,
        filters
    ):
        return cls.repository.get_filtered_legal_entities(filters)

    @staticmethod
    @transaction.atomic
    def create_legal_entity(user=None, data=None):

        data = data or {}

        legal_entity_code = data.get(
            "legal_entity_code"
        )

        OrganizationValidator.validate_code_format(
            legal_entity_code,
            "legal_entity_code",
        )



        legal_entity_unit = OrganizationUnit.objects.create(

            unit_code=legal_entity_code,

            unit_name=data.get(
                "legal_entity_name",
                legal_entity_code,
            ),

            unit_type=OrganizationUnitType.LEGAL_ENTITY,

            created_by=getattr(
                user,
                "username",
                None,
            ),
        )

        legal_entity_profile = LegalEntityProfile.objects.create(

            organization_unit=legal_entity_unit,

            legal_entity_code=legal_entity_code,

            legal_entity_name=data.get(
                "legal_entity_name",
                legal_entity_code,
            ),

            legal_name=data.get(
                "legal_name",
                "",
            ),

            registration_no=data.get(
                "registration_no",
                "",
            ),

            tax_registration_no=data.get(
                "tax_registration_no",
                "",
            ),

            country_code=data.get(
                "country_code"
            ),

            functional_currency_code=data.get(
                "functional_currency_code"
            ),

            presentation_currency_code=data.get(
                "presentation_currency_code",
                "",
            ),

            financial_year_start_month=data.get(
                "financial_year_start_month",
                4
            ),

            financial_year_start_day=data.get(
                "financial_year_start_day",
                1
            ),

            legal_form=data.get(
                "legal_form",
                ""
            ),
            is_active=data.get(
                "is_active",
                True
            ),
        )

        return legal_entity_profile
           