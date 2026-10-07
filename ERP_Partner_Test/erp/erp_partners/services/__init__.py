"""
BizSoft ERP - Partners Module

File:
    erp_partners/services/__init__.py

Purpose:
    Exports partner services.

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

from erp_partners.services.partner_service import PartnerService
from erp_partners.services.relationship_service import RelationshipService
from erp_partners.services.partner_validation_service import PartnerValidationService
