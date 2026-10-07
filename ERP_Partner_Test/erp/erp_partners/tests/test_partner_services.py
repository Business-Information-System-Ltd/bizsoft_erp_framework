"""
BizSoft ERP - Partners Module

File:
    erp_partners/tests/test_partner_services.py

Purpose:
    Tests partner service and relationship behavior.

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

class PartnerServiceTests(TestCase):
    def create_active_partner(self, code='P001', ptype=PartnerType.NATURAL_PERSON):
        partner = PartnerService.create_partner({'partner_code': code, 'partner_type': ptype, 'display_name': code})
        PartnerService.activate_partner(partner.id)
        return partner

    def test_add_multiple_roles_and_prevent_duplicate(self):
        partner = self.create_active_partner()
        PartnerService.add_role(partner.id, {'role_type': PartnerRoleType.CUSTOMER, 'status': PartnerStatus.ACTIVE})
        PartnerService.add_role(partner.id, {'role_type': PartnerRoleType.SUPPLIER, 'status': PartnerStatus.ACTIVE})
        with self.assertRaises(ValidationError):
            PartnerService.add_role(partner.id, {'role_type': PartnerRoleType.CUSTOMER, 'status': PartnerStatus.ACTIVE})

    def test_create_relationship_with_legal_entity_id(self):
        supplier = self.create_active_partner('SUP001', PartnerType.LEGAL_PERSON)
        company = self.create_active_partner('COMP001', PartnerType.LEGAL_PERSON)
        rel = RelationshipService.create_relationship({'from_partner': supplier.id, 'to_partner': company.id, 'legal_entity_id': uuid4(), 'relationship_type': RelationshipType.SUPPLIER_OF, 'relationship_category': RelationshipCategory.COMMERCIAL})
        self.assertEqual(rel.relationship_type, RelationshipType.SUPPLIER_OF)

    def test_reject_self_relationship(self):
        partner = self.create_active_partner()
        with self.assertRaises(ValidationError):
            RelationshipService.create_relationship({'from_partner': partner.id, 'to_partner': partner.id, 'legal_entity_id': uuid4(), 'relationship_type': RelationshipType.CUSTOMER_OF})

    def test_validate_partner_usage_as_customer(self):
        customer = self.create_active_partner('CUS001')
        company = self.create_active_partner('COMP002', PartnerType.LEGAL_PERSON)
        legal_entity_id = uuid4()
        PartnerService.add_role(customer.id, {'role_type': PartnerRoleType.CUSTOMER, 'status': PartnerStatus.ACTIVE})
        RelationshipService.create_relationship({'from_partner': customer.id, 'to_partner': company.id, 'legal_entity_id': legal_entity_id, 'relationship_type': RelationshipType.CUSTOMER_OF, 'relationship_category': RelationshipCategory.COMMERCIAL})
        result = PartnerValidationService.validate_partner_usage(customer.id, legal_entity_id, required_role=PartnerRoleType.CUSTOMER, required_relationship=RelationshipType.CUSTOMER_OF)
        self.assertTrue(result['valid'])

    def test_blocked_partner_usage_should_fail(self):
        partner = self.create_active_partner('BLK001')
        PartnerService.block_partner(partner.id, reason='Test block')
        result = PartnerValidationService.validate_partner_usage(partner.id, uuid4())
        self.assertFalse(result['valid'])
