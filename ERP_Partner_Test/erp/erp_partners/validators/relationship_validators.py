"""
BizSoft ERP - Partners Module

File:
    erp_partners/validators/relationship_validators.py

Purpose:
    Provides reusable partner relationship validation helpers.

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

def validate_not_self_relationship(from_partner, to_partner):
    if from_partner and to_partner and from_partner.id == to_partner.id:
        raise serializers.ValidationError('from_partner and to_partner cannot be the same.')


def validate_percentage(value):
    if value is not None and (value < 0 or value > 100):
        raise serializers.ValidationError({'percentage': 'percentage must be between 0 and 100.'})


def validate_legal_entity_first(attrs):
    if attrs.get('relationship_type') in FORMAL_RELATIONSHIP_TYPES and not attrs.get('legal_entity_id'):
        raise serializers.ValidationError({'legal_entity_id': 'legal_entity_id is required for this formal ERP relationship.'})
