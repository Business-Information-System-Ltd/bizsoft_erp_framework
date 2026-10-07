"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_role.py

Purpose:
    Defines roles that a partner can play.

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

from erp_partners.enums.partner_enums import PartnerRoleType, PartnerStatus
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerRole(BaseModel):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='roles')
    role_type = models.CharField(max_length=50, choices=PartnerRoleType.choices)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=PartnerStatus.choices, default=PartnerStatus.ACTIVE)
    is_primary_role = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['role_type']), models.Index(fields=['status'])]

    def __str__(self):
        return f'{self.partner.partner_code} - {self.role_type}'
