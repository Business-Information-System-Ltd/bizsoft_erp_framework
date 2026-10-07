"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/__init__.py

Purpose:
    Exports partner model classes.

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


from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner
from erp_partners.models.person_profile import PersonProfile
from erp_partners.models.legal_entity_profile import LegalEntityProfile
from erp_partners.models.partner_role import PartnerRole
from erp_partners.models.partner_relationship import PartnerRelationship
from erp_partners.models.partner_address import PartnerAddress
from erp_partners.models.partner_contact import PartnerContact
from erp_partners.models.partner_identification import PartnerIdentification
from erp_partners.models.partner_registration import PartnerRegistration
from erp_partners.models.partner_compliance_summary import PartnerComplianceSummary
from erp_partners.models.business_policy import BusinessPolicy
from erp_partners.models.partner_role_conflict_rule import PartnerRoleConflictRule

__all__ = [
    'BaseModel', 'Partner', 'PersonProfile', 'LegalEntityProfile', 'PartnerRole',
    'PartnerRelationship', 'PartnerAddress', 'PartnerContact', 'PartnerIdentification',
    'PartnerRegistration', 'PartnerComplianceSummary', 'BusinessPolicy', 'PartnerRoleConflictRule'
]
