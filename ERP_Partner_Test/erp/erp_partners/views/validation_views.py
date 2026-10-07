"""
BizSoft ERP - Partners Module

File:
    erp_partners/views/validation_views.py

Purpose:
    Defines partner usage validation API view.

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


from rest_framework.views import APIView
from rest_framework.response import Response

from erp_partners.serializers.validation_serializers import PartnerUsageValidationSerializer
from erp_partners.services.partner_validation_service import PartnerValidationService


class PartnerUsageValidationView(APIView):
    def post(self, request):
        serializer = PartnerUsageValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PartnerValidationService.validate_partner_usage(**serializer.validated_data)
        return Response(result)
