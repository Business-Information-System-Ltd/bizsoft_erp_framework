# from rest_framework import serializers


# class CreatePartnerWithContextSerializer(
#     serializers.Serializer
# ):
#     partner = serializers.DictField()

#     role = serializers.DictField(
#         required=False
#     )

#     relationship = serializers.DictField(
#         required=False
#     )


from rest_framework import serializers

from erp_partners.serializers.partner_compliance_serializers import PartnerComplianceSummarySerializer
from erp_partners.serializers.partner_address_serializers import (
    PartnerAddressSerializer
)
from erp_partners.serializers.partner_contact_serializers import (
    PartnerContactSerializer
)
from erp_partners.serializers.partner_identification_serializers import (
    PartnerIdentificationSerializer
)
from erp_partners.serializers.partner_registration_serializers import (
    PartnerRegistrationSerializer
)


class CreatePartnerWithContextSerializer(serializers.Serializer):

    partner = serializers.DictField()

    role = serializers.DictField(
        required=False
    )

    relationship = serializers.DictField(
        required=False
    )

    addresses = PartnerAddressSerializer(
        many=True,
        required=False
    )

    contacts = PartnerContactSerializer(
        many=True,
        required=False
    )

    identifications = PartnerIdentificationSerializer(
        many=True,
        required=False
    )

    registrations = PartnerRegistrationSerializer(
        many=True,
        required=False
    )
    compliance_summary = PartnerComplianceSummarySerializer(
        required=False  
    )