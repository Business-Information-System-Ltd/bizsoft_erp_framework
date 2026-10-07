"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/legal_entity_profile_serializers.py

Purpose:
    Defines serializers for legal entity profile.

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

from erp_partners.enums.partner_enums import PartnerType
from erp_partners.models import LegalEntityProfile


class LegalEntityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntityProfile
        fields = '__all__'

    def validate(self, attrs):
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        if partner and partner.partner_type not in {PartnerType.LEGAL_PERSON, PartnerType.GOVERNMENT_BODY, PartnerType.INTERNAL_ORGANIZATION}:
            raise serializers.ValidationError('LegalEntityProfile is only allowed for legal, government, or internal organization partners.')
        if not attrs.get('legal_name') and not getattr(self.instance, 'legal_name', None):
            raise serializers.ValidationError({'legal_name': 'legal_name is required.'})
        return attrs
