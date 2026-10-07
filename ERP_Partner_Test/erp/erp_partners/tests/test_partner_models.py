"""
BizSoft ERP - Partners Module

File:
    erp_partners/tests/test_partner_models.py

Purpose:
    Tests partner model and serializer validation.

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


from datetime import date
from uuid import uuid4

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from erp_partners.enums.partner_enums import ContactType, IdentificationType, PartnerRoleType, PartnerStatus, PartnerType, RelationshipCategory, RelationshipType
from erp_partners.models import LegalEntityProfile, Partner, PersonProfile
from erp_partners.serializers import LegalEntityProfileSerializer, PartnerContactSerializer, PartnerIdentificationSerializer, PersonProfileSerializer
from erp_partners.services.partner_service import PartnerService
from erp_partners.services.partner_validation_service import PartnerValidationService
from erp_partners.services.relationship_service import RelationshipService

class PartnerModelTests(TestCase):
    def test_create_natural_person_partner(self):
        partner = PartnerService.create_partner({'partner_code':'P001','partner_type':PartnerType.NATURAL_PERSON,'display_name':'U Aung Aung'})
        profile = PersonProfile.objects.create(partner=partner, full_name='U Aung Aung')
        self.assertEqual(profile.partner.partner_type, PartnerType.NATURAL_PERSON)

    def test_create_legal_entity_partner(self):
        partner = PartnerService.create_partner({'partner_code':'C001','partner_type':PartnerType.LEGAL_PERSON,'display_name':'ABC Trading'})
        profile = LegalEntityProfile.objects.create(partner=partner, legal_name='ABC Trading Co., Ltd.')
        self.assertEqual(profile.legal_name, 'ABC Trading Co., Ltd.')

    def test_reject_person_profile_for_legal_entity_partner(self):
        partner = Partner.objects.create(partner_code='C002', partner_type=PartnerType.LEGAL_PERSON, display_name='ABC')
        serializer = PersonProfileSerializer(data={'partner': partner.id, 'full_name': 'ABC'})
        self.assertFalse(serializer.is_valid())

    def test_reject_legal_entity_profile_for_natural_person_partner(self):
        partner = Partner.objects.create(partner_code='P002', partner_type=PartnerType.NATURAL_PERSON, display_name='U Aung')
        serializer = LegalEntityProfileSerializer(data={'partner': partner.id, 'legal_name': 'Bad Co'})
        self.assertFalse(serializer.is_valid())

    def test_validate_email_contact(self):
        partner = Partner.objects.create(partner_code='P003', partner_type=PartnerType.NATURAL_PERSON, display_name='U Aung')
        serializer = PartnerContactSerializer(data={'partner': partner.id, 'contact_type': ContactType.EMAIL, 'contact_value': 'bad-email'})
        self.assertFalse(serializer.is_valid())

    def test_expiry_date_before_issue_date_should_fail(self):
        partner = Partner.objects.create(partner_code='P004', partner_type=PartnerType.NATURAL_PERSON, display_name='U Aung')
        serializer = PartnerIdentificationSerializer(data={'partner': partner.id, 'identification_type': IdentificationType.PASSPORT, 'identification_no': 'A123', 'issue_date': '2026-06-04', 'expiry_date': '2026-06-03'})
        self.assertFalse(serializer.is_valid())
