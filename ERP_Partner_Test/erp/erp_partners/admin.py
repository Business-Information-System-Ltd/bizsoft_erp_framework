"""
BizSoft ERP - Partners Module

File:
    erp_partners/admin.py

Purpose:
    Registers partner models with Django admin.

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


from django.contrib import admin

from erp_partners.models import (
    LegalEntityProfile,
    Partner,
    PartnerAddress,
    PartnerComplianceSummary,
    PartnerContact,
    PartnerIdentification,
    PartnerRegistration,
    PartnerRelationship,
    PartnerRole,
    PersonProfile,
)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('partner_code', 'display_name', 'partner_type', 'status', 'is_active', 'created_at')
    search_fields = ('partner_code', 'display_name', 'legal_name', 'short_name')
    list_filter = ('partner_type', 'status', 'is_active')


for model in [PersonProfile, LegalEntityProfile, PartnerRole, PartnerRelationship, PartnerAddress, PartnerContact, PartnerIdentification, PartnerRegistration, PartnerComplianceSummary]:
    admin.site.register(model)
