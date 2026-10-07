from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from erp_partners.serializers.create_partner_with_context_serializer import (
    CreatePartnerWithContextSerializer
)

from erp_partners.services.partner_service import (
    PartnerService
)
from erp_partners.serializers.partner_serializers import (
    PartnerDetailSerializer
)

class CreatePartnerWithContextAPIView(
    APIView
):

    def post(self, request):

        serializer = (
            CreatePartnerWithContextSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = (
            PartnerService
            .create_with_context(
                partner_data=serializer.validated_data[
                    "partner"
                ],
                role_data=serializer.validated_data.get(
                    "role"
                ),
                addresses_data=serializer.validated_data.get(
                    "addresses",
                    []
                ),

                contacts_data=serializer.validated_data.get(
                    "contacts",
                    []
                ),

                identifications_data=serializer.validated_data.get(
                    "identifications",
                    []
                ),

                registrations_data=serializer.validated_data.get(
                    "registrations",
                    []
                ),
                relationship_data=serializer.validated_data.get(
                    "relationship"
                ),
                compliance_summary_data=serializer.validated_data.get(
                    "compliance_summary"
                ),
                created_by=str(request.user)
                # created_by=(
                #     str(request.user)
                #     if request.user.is_authenticated
                #     else None
                # )
            )
        )

        return Response(
            {
                "message": "Partner created successfully",
                "partner": PartnerDetailSerializer(
                    result["partner"]
                ).data,
                "role_id": (
                    result["role"].id
                    if result["role"]
                    else None
                ),
                "relationship_id": (
                    result["relationship"].id
                    if result["relationship"]
                    else None
                ),
            },
            status=status.HTTP_201_CREATED
        )