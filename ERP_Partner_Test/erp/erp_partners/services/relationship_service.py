"""
BizSoft ERP - Partners Module

File:
    erp_partners/services/relationship_service.py

Purpose:
    Provides transaction-safe partner relationship service methods.

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


from django.db import transaction
from rest_framework.exceptions import NotFound

from erp_partners.models import PartnerRelationship
from erp_partners.repositories.relationship_repository import RelationshipRepository
from erp_partners.serializers.partner_relationship_serializers import PartnerRelationshipSerializer


class RelationshipService:
    repository = RelationshipRepository()

    @classmethod
    @transaction.atomic
    def create_relationship(cls, data, created_by=None):
        """Create a relationship after serializer validation."""
        serializer = PartnerRelationshipSerializer(data={**data, 'created_by': created_by})
        serializer.is_valid(raise_exception=True)
        return cls.repository.create(serializer.validated_data)

    @classmethod
    @transaction.atomic
    def end_relationship(cls, relationship_id, effective_to, updated_by=None):
        relationship = PartnerRelationship.objects.filter(id=relationship_id).first()
        if not relationship:
            raise NotFound('Partner relationship not found.')
        relationship.effective_to = effective_to
        relationship.updated_by = updated_by
        relationship.save(update_fields=['effective_to', 'updated_by', 'updated_at'])
        return relationship

    @classmethod
    def get_active_relationships(cls, partner_id):
        return cls.repository.get_active_relationships(partner_id)
