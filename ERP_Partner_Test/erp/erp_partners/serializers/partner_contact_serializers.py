"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_contact_serializers.py

Purpose:
    Defines serializers for partner contacts.

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


from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from erp_partners.enums.partner_enums import ContactType
from erp_partners.models import PartnerContact
from erp_partners.validators.partner_validators import validate_date_range


class PartnerContactSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerContact
        fields = '__all__'

    def validate(self, attrs):
        attrs = validate_date_range(attrs)
        contact_type = attrs.get('contact_type') or getattr(self.instance, 'contact_type', None)
        contact_value = attrs.get('contact_value') or getattr(self.instance, 'contact_value', None)
        if not contact_value:
            raise serializers.ValidationError({'contact_value': 'contact_value is required.'})
        if contact_type == ContactType.EMAIL:
            try:
                validate_email(contact_value)
            except DjangoValidationError as exc:
                raise serializers.ValidationError({'contact_value': 'Enter a valid email address.'}) from exc
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        if attrs.get('is_primary') and partner and contact_type:
            qs = PartnerContact.objects.filter(partner=partner, contact_type=contact_type, is_primary=True, is_active=True)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError('Only one primary contact is allowed per partner and contact_type.')
        return attrs
