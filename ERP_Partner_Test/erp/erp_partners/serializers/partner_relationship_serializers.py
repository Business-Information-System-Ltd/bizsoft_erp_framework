"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_relationship_serializers.py

Purpose:
    Defines serializers for partner relationships.

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


from rest_framework import serializers

from erp_partners.models import PartnerRelationship
from erp_partners.validators.partner_validators import validate_date_range
from erp_partners.validators.relationship_validators import validate_legal_entity_first, validate_not_self_relationship, validate_percentage


class PartnerRelationshipSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerRelationship
        fields = '__all__'

    def validate(self, attrs):
        attrs = validate_date_range(attrs)
        validate_not_self_relationship(attrs.get('from_partner') or getattr(self.instance, 'from_partner', None), attrs.get('to_partner') or getattr(self.instance, 'to_partner', None))
        validate_percentage(attrs.get('percentage'))
        validate_legal_entity_first(attrs)
        return attrs
