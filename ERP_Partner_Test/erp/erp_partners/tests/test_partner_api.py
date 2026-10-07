"""
BizSoft ERP - Partners Module

File:
    erp_partners/tests/test_partner_api.py

Purpose:
    Tests partner API endpoints.

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

class PartnerApiTests(TestCase):
    def test_create_partner_api(self):
        client = APIClient()
        response = client.post('/api/partners/', {'partner_code': 'API001', 'partner_type': PartnerType.LEGAL_PERSON, 'display_name': 'API Co'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['partner_code'], 'API001')
