from rest_framework import viewsets

from erp_partners.models.legal_entity_profile import LegalEntityProfile
from erp_partners.serializers.legal_entity_profile_serializers import (
    LegalEntityProfileSerializer
)

class LegalEntityProfileViewSet(viewsets.ModelViewSet):
    queryset = LegalEntityProfile.objects.all()
    serializer_class = LegalEntityProfileSerializer