"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_role_serializers.py

Purpose:
    Defines serializers for partner roles.

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

from erp_partners.models import PartnerRole
from erp_partners.validators.partner_validators import validate_date_range, validate_partner_status_for_role


class PartnerRoleSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = PartnerRole
        fields = '__all__'
        extra_kwargs = {
        'partner': {
            'required': False,
            'allow_null': True,
            },
        }

    def validate(self, attrs):
        attrs = validate_date_range(attrs)
        partner = attrs.get('partner') or getattr(self.instance, 'partner', None)
        role_type = attrs.get('role_type') or getattr(self.instance, 'role_type', None)
        if partner:
            validate_partner_status_for_role(partner)
        if partner and role_type:
            qs = PartnerRole.objects.filter(partner=partner, role_type=role_type, is_active=True)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError('Partner already has this active role_type.')
        return attrs
