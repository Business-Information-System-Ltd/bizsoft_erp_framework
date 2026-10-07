"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_address.py

Purpose:
    Defines partner address records.

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

from erp_partners.enums.partner_enums import AddressType
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerAddress(BaseModel):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=30, choices=AddressType.choices)
    country_code = models.CharField(max_length=10, blank=True)
    state_region = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    township = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    ward_village = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=255, blank=True)
    building_no = models.CharField(max_length=100, blank=True)
    room_no = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.partner.partner_code} - {self.address_type}'
