from rest_framework import serializers

from erp_partners.models import Partner
from erp_partners.serializers.partner_role_serializers import (
    PartnerRoleSerializer,
)
from erp_partners.serializers.partner_relationship_serializers import (
    PartnerRelationshipSerializer,
)


class PartnerSummarySerializer(serializers.ModelSerializer):
    roles = PartnerRoleSerializer(
        many=True,
        read_only=True,
    )

    relationships = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = (
            "id",
            "partner_code",
            "display_name",
            "partner_type",
            "status",
            "roles",
            "relationships",
        )

    def get_relationships(self, obj):
        return PartnerRelationshipSerializer(
            obj.relationships_from.filter(
                is_active=True
            ),
            many=True,
        ).data