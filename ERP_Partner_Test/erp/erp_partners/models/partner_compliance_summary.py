"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_compliance_summary.py

Purpose:
    Defines summary compliance status for partners.

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

from erp_partners.enums.partner_enums import KYCStatus, RiskLevel, ScreeningStatus
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerComplianceSummary(BaseModel):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='compliance_summary')
    kyc_status = models.CharField(max_length=30, choices=KYCStatus.choices, default=KYCStatus.NOT_REQUIRED)
    risk_level = models.CharField(max_length=30, choices=RiskLevel.choices, default=RiskLevel.NOT_ASSESSED)
    pep_status = models.CharField(max_length=30, choices=ScreeningStatus.choices, default=ScreeningStatus.NOT_SCREENED)
    sanctions_screening_status = models.CharField(max_length=30, choices=ScreeningStatus.choices, default=ScreeningStatus.NOT_SCREENED)
    blacklist_status = models.CharField(max_length=30, choices=ScreeningStatus.choices, default=ScreeningStatus.NOT_SCREENED)
    related_party_status = models.CharField(max_length=30, choices=ScreeningStatus.choices, default=ScreeningStatus.NOT_SCREENED)
    beneficial_owner_verified = models.BooleanField(default=False)
    last_review_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.partner.partner_code} compliance'
