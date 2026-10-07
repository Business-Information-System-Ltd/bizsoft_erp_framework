"""
BizSoft ERP - Partners Module

File:
    erp_partners/views/relationship_views.py

Purpose:
    Defines partner relationship API ViewSet.

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


from rest_framework import status, viewsets
from rest_framework.response import Response

from erp_partners.models import PartnerRelationship
from erp_partners.serializers.partner_relationship_serializers import PartnerRelationshipSerializer
from erp_partners.services.relationship_service import RelationshipService


class PartnerRelationshipViewSet(viewsets.ModelViewSet):
    queryset = PartnerRelationship.objects.all().order_by('-created_at')
    serializer_class = PartnerRelationshipSerializer

    def create(self, request, *args, **kwargs):
        relationship = RelationshipService.create_relationship(request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerRelationshipSerializer(relationship).data, status=status.HTTP_201_CREATED)
