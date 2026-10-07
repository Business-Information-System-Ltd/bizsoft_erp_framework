"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_address_serializers.py

Purpose:
    Defines serializers for partner addresses.

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

from erp_partners.models import PartnerAddress
from erp_partners.validators.partner_validators import validate_date_range


class PartnerAddressSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerAddress
        fields = '__all__'
        extra_kwargs = {
            'partner': {
                'required': False,
                'allow_null': True,
            },
        }

    def validate(self, attrs):
        attrs = validate_date_range(attrs)
        if not attrs.get('full_address') and not getattr(self.instance, 'full_address', None):
            raise serializers.ValidationError({'full_address': 'full_address is required.'})
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        address_type = attrs.get('address_type') or getattr(self.instance, 'address_type', None)
        if attrs.get('is_primary') and partner and address_type:
            qs = PartnerAddress.objects.filter(partner=partner, address_type=address_type, is_primary=True, is_active=True)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError('Only one primary address is allowed per partner and address_type.')
        return attrs
