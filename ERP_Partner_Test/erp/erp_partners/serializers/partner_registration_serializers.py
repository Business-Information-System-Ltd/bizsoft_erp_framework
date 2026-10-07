"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_registration_serializers.py

Purpose:
    Defines serializers for partner registrations.

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

from erp_partners.models import PartnerRegistration
from erp_partners.validators.partner_validators import validate_issue_expiry


class PartnerRegistrationSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerRegistration
        fields = '__all__'

    def validate(self, attrs):
        attrs = validate_issue_expiry(attrs)
        if not attrs.get('registration_no') and not getattr(self.instance, 'registration_no', None):
            raise serializers.ValidationError({'registration_no': 'registration_no is required.'})
        return attrs
