from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from erp_partners.models import Partner

from erp_partners.serializers.role_conflict_serializer import (
    ValidateRoleChangeSerializer
)

from erp_partners.services.role_conflict_service import (
    RoleConflictService
)


class ValidateRoleChangeAPIView(
    APIView
):

    def post(self, request):

        serializer = (
            ValidateRoleChangeSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        partner = Partner.objects.get(
            id=serializer.validated_data[
                "partner_id"
            ]
        )

        result = (
            RoleConflictService
            .validate_role_change(
                partner_id=partner.id,
                new_role=serializer.validated_data[
                    "new_role"
                ]
            )
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )