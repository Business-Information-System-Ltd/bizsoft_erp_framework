from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from erp_partners.serializers.check_duplicate_serializer import (
    CheckDuplicateSerializer
)

from erp_partners.services.duplicate_check_service import (
    DuplicateCheckService
)


class CheckDuplicateAPIView(
    APIView
):

    def post(self, request):

        serializer = (
            CheckDuplicateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = (
            DuplicateCheckService
            .check_duplicate(
                serializer.validated_data
            )
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )