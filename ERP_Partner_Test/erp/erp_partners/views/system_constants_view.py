from rest_framework.views import APIView
from rest_framework.response import Response

from erp_partners.enums.partner_enums import (
    PartnerType,
    PartnerRoleType
)


class SystemConstantsAPIView(
    APIView
):

    def get(self, request):

        return Response(
            {
                "partner_types": [
                    item[0]
                    for item in
                    PartnerType.choices
                ],

                "role_types": [
                    item[0]
                    for item in
                    PartnerRoleType.choices
                ],

                "duplicate_check_fields": [
                    "name",
                    "phone_no",
                    "email",
                    "father_name",
                    "registration_no",
                    "tax_id"
                ]
            }
        )