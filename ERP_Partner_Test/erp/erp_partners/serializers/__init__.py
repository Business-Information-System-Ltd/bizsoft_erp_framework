"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/__init__.py

Purpose:
    Exports partner serializers.

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


from erp_partners.serializers.partner_serializers import PartnerDetailSerializer, PartnerSerializer
from erp_partners.serializers.person_profile_serializers import PersonProfileSerializer
from erp_partners.serializers.legal_entity_profile_serializers import LegalEntityProfileSerializer
from erp_partners.serializers.partner_role_serializers import PartnerRoleSerializer
from erp_partners.serializers.partner_relationship_serializers import PartnerRelationshipSerializer
from erp_partners.serializers.partner_address_serializers import PartnerAddressSerializer
from erp_partners.serializers.partner_contact_serializers import PartnerContactSerializer
from erp_partners.serializers.partner_identification_serializers import PartnerIdentificationSerializer
from erp_partners.serializers.partner_registration_serializers import PartnerRegistrationSerializer
from erp_partners.serializers.partner_compliance_serializers import PartnerComplianceSummarySerializer
from erp_partners.serializers.validation_serializers import PartnerUsageValidationSerializer
