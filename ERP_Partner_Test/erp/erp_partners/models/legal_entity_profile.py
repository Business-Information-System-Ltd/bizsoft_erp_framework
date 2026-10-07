"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/legal_entity_profile.py

Purpose:
    Defines legal person profile data for a partner.

Architectural Notes:
    - This module manages common Business Partner / Stakeholder master data.
    - Customer, Supplier, Employee, FAR, Finance, and other module-specific profiles
      must be implemented in their respective modules.
    - This module should remain a core shared service with minimum external dependency.

Author:
    BizSoft Systems

Created:
    2026-06-04
"""


from django.db import models

from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class LegalEntityProfile(BaseModel):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='legal_entity_profile')
    legal_entity_type = models.CharField(max_length=100, blank=True)
    legal_name = models.CharField(max_length=255)
    trading_name = models.CharField(max_length=255, blank=True)
    registration_no = models.CharField(max_length=100, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    incorporation_country = models.CharField(max_length=10, blank=True)
    incorporation_place = models.CharField(max_length=255, blank=True)
    legal_form = models.CharField(max_length=100, blank=True)
    business_sector = models.CharField(max_length=150, blank=True)
    industry_type = models.CharField(max_length=150, blank=True)
    ownership_type = models.CharField(max_length=150, blank=True)
    company_size = models.CharField(max_length=100, blank=True)
    financial_year_start_month = models.PositiveSmallIntegerField(null=True, blank=True)
    financial_year_end_month = models.PositiveSmallIntegerField(null=True, blank=True)
    tax_identification_no = models.CharField(max_length=100, blank=True)
    commercial_tax_no = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.legal_name
