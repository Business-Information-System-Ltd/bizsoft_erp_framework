from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from erp_partners.models import Partner, PartnerComplianceSummary
from erp_partners.serializers.partner_compliance_serializers import (
    PartnerComplianceSummarySerializer,
)


class PartnerComplianceSummaryAPIView(APIView):

    def get_partner(self, partner_id):
        try:
            return Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return None

    def get(self, request, partner_id):

        partner = self.get_partner(partner_id)

        if not partner:
            return Response(
                {"detail": "Partner not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            compliance = partner.compliance_summary
        except PartnerComplianceSummary.DoesNotExist:
            return Response(
                {
                    "partner_id": str(partner.id),
                    "compliance_summary": None
                },
                status=status.HTTP_200_OK
            )

        return Response(
            PartnerComplianceSummarySerializer(compliance).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, partner_id):

        partner = self.get_partner(partner_id)

        if not partner:
            return Response(
                {"detail": "Partner not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if PartnerComplianceSummary.objects.filter(
            partner=partner
        ).exists():

            return Response(
                {
                    "detail": "Compliance summary already exists for this partner."
                },
                status=status.HTTP_409_CONFLICT
            )

        serializer = PartnerComplianceSummarySerializer(
            data={
                **request.data,
                "partner": partner.id,
                "created_by": str(request.user),
            }
        )

        serializer.is_valid(raise_exception=True)

        compliance = serializer.save()

        return Response(
            PartnerComplianceSummarySerializer(compliance).data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, partner_id):

        return self._update(
            request,
            partner_id,
            partial=False
        )

    def patch(self, request, partner_id):

        return self._update(
            request,
            partner_id,
            partial=True
        )

    def _update(
        self,
        request,
        partner_id,
        partial=False
    ):

        partner = self.get_partner(partner_id)

        if not partner:
            return Response(
                {"detail": "Partner not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            compliance = partner.compliance_summary
        except PartnerComplianceSummary.DoesNotExist:
            return Response(
                {"detail": "Compliance summary not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PartnerComplianceSummarySerializer(
            compliance,
            data={
                **request.data,
                "updated_by": str(request.user),
            },
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        compliance = serializer.save()

        return Response(
            PartnerComplianceSummarySerializer(compliance).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, partner_id):

        partner = self.get_partner(partner_id)

        if not partner:
            return Response(
                {"detail": "Partner not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            compliance = partner.compliance_summary
        except PartnerComplianceSummary.DoesNotExist:
            return Response(
                {"detail": "Compliance summary not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        compliance.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )