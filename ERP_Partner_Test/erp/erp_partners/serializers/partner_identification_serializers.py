"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_identification_serializers.py

Purpose:
    Defines serializers for partner identifications.

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

from erp_partners.models import PartnerIdentification
from erp_partners.validators.partner_validators import validate_issue_expiry


class PartnerIdentificationSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerIdentification
        fields = '__all__'

    def validate(self, attrs):
        attrs = validate_issue_expiry(attrs)
        if not attrs.get('identification_no') and not getattr(self.instance, 'identification_no', None):
            raise serializers.ValidationError({'identification_no': 'identification_no is required.'})
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        identification_type = attrs.get('identification_type') or getattr(self.instance, 'identification_type', None)
        if attrs.get('is_primary') and partner and identification_type:
            qs = PartnerIdentification.objects.filter(partner=partner, identification_type=identification_type, is_primary=True, is_active=True)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError('Only one primary identification is allowed per partner and identification_type.')
        return attrs
