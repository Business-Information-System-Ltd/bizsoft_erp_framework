"""
BizSoft ERP - Partners Module

File:
    erp_partners/views/__init__.py

Purpose:
    Exports partner API views.

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

from erp_partners.views.partner_views import PartnerViewSet
from erp_partners.views.relationship_views import PartnerRelationshipViewSet
from erp_partners.views.validation_views import PartnerUsageValidationView
