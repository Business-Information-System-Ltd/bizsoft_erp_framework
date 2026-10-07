"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner.py

Purpose:
    Defines the centralized Partner master model.

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

from erp_partners.enums.partner_enums import PartnerStatus, PartnerType
from erp_partners.models.base import BaseModel


class Partner(BaseModel):
    partner_code = models.CharField(max_length=50, unique=True, db_index=True)
    partner_type = models.CharField(max_length=30, choices=PartnerType.choices)
    display_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=PartnerStatus.choices, default=PartnerStatus.DRAFT)
    country_code = models.CharField(max_length=10, blank=True)
    default_language = models.CharField(max_length=20, blank=True)
    default_currency_code = models.CharField(max_length=10, blank=True)
    external_reference = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['partner_code']
        indexes = [models.Index(fields=['partner_type']), models.Index(fields=['status']), models.Index(fields=['display_name'])]

    def __str__(self):
        return f'{self.partner_code} - {self.display_name}'
