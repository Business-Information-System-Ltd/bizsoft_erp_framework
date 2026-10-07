"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_contact.py

Purpose:
    Defines partner contact records.

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

from erp_partners.enums.partner_enums import ContactType
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerContact(BaseModel):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=30, choices=ContactType.choices)
    contact_value = models.CharField(max_length=255)
    contact_label = models.CharField(max_length=100, blank=True)
    department_name = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.partner.partner_code} - {self.contact_type}'
