"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/person_profile_serializers.py

Purpose:
    Defines serializers for natural person profile.

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
from erp_partners.models import PersonProfile


class PersonProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonProfile
        fields = '__all__'

    def validate(self, attrs):
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        if partner and partner.partner_type != PartnerType.NATURAL_PERSON:
            raise serializers.ValidationError('PersonProfile is only allowed for NATURAL_PERSON partners.')
        if not attrs.get('full_name') and not getattr(self.instance, 'full_name', None):
            raise serializers.ValidationError({'full_name': 'full_name is required.'})
        return attrs
