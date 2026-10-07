"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_identification.py

Purpose:
    Defines partner identification records.

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

from erp_partners.enums.partner_enums import IdentificationType
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerIdentification(BaseModel):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='identifications')
    identification_type = models.CharField(max_length=40, choices=IdentificationType.choices)
    identification_no = models.CharField(max_length=150)
    issuing_country = models.CharField(max_length=10, blank=True)
    issuing_authority = models.CharField(max_length=255, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    document_file_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f'{self.partner.partner_code} - {self.identification_type}'
