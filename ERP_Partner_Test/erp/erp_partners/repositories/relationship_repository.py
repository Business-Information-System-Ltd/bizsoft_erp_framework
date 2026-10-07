"""
BizSoft ERP - Partners Module

File:
    erp_partners/repositories/relationship_repository.py

Purpose:
    Provides persistence access for partner relationships.

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


from django.utils import timezone

from erp_partners.enums.partner_enums import PartnerStatus
from erp_partners.models import PartnerRelationship


class RelationshipRepository:
    def get_active_relationships(self, partner_id):
        return PartnerRelationship.objects.filter(from_partner_id=partner_id, is_active=True, status=PartnerStatus.ACTIVE)

    def get_relationships_by_legal_entity(self, legal_entity_id):
        return PartnerRelationship.objects.filter(legal_entity_id=legal_entity_id, is_active=True)

    def has_active_relationship(self, partner_id, legal_entity_id, relationship_type, as_of_date=None):
        as_of_date = as_of_date or timezone.localdate()
        qs = PartnerRelationship.objects.filter(
            from_partner_id=partner_id,
            legal_entity_id=legal_entity_id,
            relationship_type=relationship_type,
            is_active=True,
            status=PartnerStatus.ACTIVE,
        )
        qs = qs.filter(effective_from__isnull=True) | qs.filter(effective_from__lte=as_of_date)
        qs = qs.filter(effective_to__isnull=True) | qs.filter(effective_to__gte=as_of_date)
        return qs.exists()

    def create(self, data):
        return PartnerRelationship.objects.create(**data)
