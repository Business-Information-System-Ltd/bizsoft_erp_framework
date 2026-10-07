"""
BizSoft ERP - Partners Module

File:
    erp_partners/validators/partner_validators.py

Purpose:
    Provides reusable partner validation helpers.

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


from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from erp_partners.enums.partner_enums import ContactType, PartnerStatus, PartnerType, RelationshipType

FORMAL_RELATIONSHIP_TYPES = {
    RelationshipType.CUSTOMER_OF, RelationshipType.SUPPLIER_OF, RelationshipType.EMPLOYEE_OF,
    RelationshipType.DIRECTOR_OF, RelationshipType.SHAREHOLDER_OF, RelationshipType.BANKER_OF,
    RelationshipType.AUDITOR_OF, RelationshipType.CONSULTANT_OF, RelationshipType.REGULATOR_OF,
    RelationshipType.SERVICE_PROVIDER_OF,
}


def validate_date_range(attrs, start='effective_from', end='effective_to'):
    if attrs.get(start) and attrs.get(end) and attrs[end] < attrs[start]:
        raise serializers.ValidationError({end: f'{end} must be greater than or equal to {start}.'})
    return attrs


def validate_issue_expiry(attrs):
    if attrs.get('issue_date') and attrs.get('expiry_date') and attrs['expiry_date'] <= attrs['issue_date']:
        raise serializers.ValidationError({'expiry_date': 'expiry_date must be later than issue_date.'})
    return attrs

def validate_partner_can_have_person_profile(partner):
    if partner.partner_type != PartnerType.NATURAL_PERSON:
        raise serializers.ValidationError('PersonProfile is only allowed for NATURAL_PERSON partners.')


def validate_partner_can_have_legal_entity_profile(partner):
    if partner.partner_type not in {PartnerType.LEGAL_PERSON, PartnerType.GOVERNMENT_BODY, PartnerType.INTERNAL_ORGANIZATION}:
        raise serializers.ValidationError('LegalEntityProfile is only allowed for legal, government, or internal organization partners.')


def validate_partner_status_for_role(partner):
    if partner.status not in {PartnerStatus.DRAFT, PartnerStatus.ACTIVE}:
        raise serializers.ValidationError('Partner must be active or draft when adding a role.')
