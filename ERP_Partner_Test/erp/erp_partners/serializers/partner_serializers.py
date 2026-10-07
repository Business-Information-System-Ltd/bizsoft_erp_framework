"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_serializers.py

Purpose:
    Defines serializers for Partner list, create/update, and detail output.

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

from erp_partners.models import Partner
from erp_partners.serializers.legal_entity_profile_serializers import LegalEntityProfileSerializer
from erp_partners.serializers.partner_address_serializers import PartnerAddressSerializer
from erp_partners.serializers.partner_compliance_serializers import PartnerComplianceSummarySerializer
from erp_partners.serializers.partner_contact_serializers import PartnerContactSerializer
from erp_partners.serializers.partner_identification_serializers import PartnerIdentificationSerializer
from erp_partners.serializers.partner_registration_serializers import PartnerRegistrationSerializer
from erp_partners.serializers.partner_role_serializers import PartnerRoleSerializer
from erp_partners.serializers.person_profile_serializers import PersonProfileSerializer


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('partner_type') and not getattr(self.instance, 'partner_type', None):
            raise serializers.ValidationError({'partner_type': 'partner_type is required.'})
        if not attrs.get('display_name') and not getattr(self.instance, 'display_name', None):
            raise serializers.ValidationError({'display_name': 'display_name is required.'})
        return attrs


class PartnerDetailSerializer(PartnerSerializer):
    person_profile = PersonProfileSerializer(read_only=True)
    legal_entity_profile = LegalEntityProfileSerializer(read_only=True)
    roles = PartnerRoleSerializer(many=True, read_only=True)
    addresses = PartnerAddressSerializer(many=True, read_only=True)
    contacts = PartnerContactSerializer(many=True, read_only=True)
    identifications = PartnerIdentificationSerializer(many=True, read_only=True)
    registrations = PartnerRegistrationSerializer(many=True, read_only=True)
    compliance_summary = PartnerComplianceSummarySerializer(read_only=True)

    class Meta(PartnerSerializer.Meta):
        fields = '__all__'
