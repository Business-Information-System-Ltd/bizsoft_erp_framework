from rest_framework import serializers


class CheckDuplicateSerializer(
    serializers.Serializer
):
    full_name = serializers.CharField(
        required=False
    )

    phone_no = serializers.CharField(
        required=False
    )

    email = serializers.EmailField(
        required=False
    )