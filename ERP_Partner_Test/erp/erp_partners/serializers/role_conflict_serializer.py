from rest_framework import serializers


class ValidateRoleChangeSerializer(
    serializers.Serializer
):
    partner_id = serializers.UUIDField()

    new_role = serializers.CharField(
        max_length=50
    )

    legal_entity_id = (
        serializers.UUIDField(
            required=False
        )
    )

    organization_unit_id = (
        serializers.UUIDField(
            required=False
        )
    )