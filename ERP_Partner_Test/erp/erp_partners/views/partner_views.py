"""
BizSoft ERP - Partners Module

File:
    erp_partners/views/partner_views.py

Purpose:
    Defines partner API ViewSet and child collection actions.

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


# from django.db.models import Q
# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from erp_partners.models import Partner, PartnerAddress, PartnerContact, PartnerIdentification, PartnerRegistration, PartnerRole
# from erp_partners.serializers import (
#     PartnerAddressSerializer,
#     PartnerContactSerializer,
#     PartnerDetailSerializer,
#     PartnerIdentificationSerializer,
#     PartnerRegistrationSerializer,
#     PartnerRoleSerializer,
#     PartnerSerializer,
# )
# from erp_partners.services.partner_service import PartnerService
# from erp_partners.serializers.partner_summary_serializers import (
#     PartnerSummarySerializer,
# )
# # from erp_partners.services.policy_check_service import PolicyCheckService
# from erp_partners.services.role_conflict_service import RoleConflictService

from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_partners.models import (
    Partner,
    PartnerAddress,
    PartnerContact,
    PartnerIdentification,
    PartnerRegistration,
    PartnerRole,
    PartnerComplianceSummary,
)

from erp_partners.serializers import (
    PartnerAddressSerializer,
    PartnerContactSerializer,
    PartnerDetailSerializer,
    PartnerIdentificationSerializer,
    PartnerRegistrationSerializer,
    PartnerRoleSerializer,
    PartnerSerializer,
)

from erp_partners.serializers.partner_compliance_serializers import (
    PartnerComplianceSummarySerializer,
)

from erp_partners.services.partner_service import PartnerService

from erp_partners.serializers.partner_summary_serializers import (
    PartnerSummarySerializer,
)

from erp_partners.services.role_conflict_service import (
    RoleConflictService,
)

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by('partner_code')
    serializer_class = PartnerSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartnerDetailSerializer
        return PartnerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        partner_type = self.request.query_params.get('partner_type')
        role_type = self.request.query_params.get('role_type')
        status_value = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        if partner_type:
            qs = qs.filter(partner_type=partner_type)
        if role_type:
            qs = qs.filter(roles__role_type=role_type, roles__is_active=True).distinct()
        if status_value:
            qs = qs.filter(status=status_value)
        if search:
            qs = qs.filter(Q(partner_code__icontains=search) | Q(display_name__icontains=search) | Q(legal_name__icontains=search) | Q(short_name__icontains=search))
        return qs

    # def create(self, request, *args, **kwargs):
    #     partner = PartnerService.create_partner(request.data, created_by=str(request.user) if request.user.is_authenticated else None)
    #     return Response(PartnerSerializer(partner).data, status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):

        created_by = (
            str(request.user)
            if request.user.is_authenticated
            else None
        )

        data = request.data

        # Support both:
        # 1. {"partner": {...}}
        # 2. {"partner_code": "...", ...}
        partner_data = data.get("partner")

        if partner_data is None:
            partner_data = {
                key: value
                for key, value in data.items()
                if key not in [
                    "roles",
                    "addresses",
                    "contacts",
                    "identifications",
                    "registrations",
                    "compliance_summary"
                ]
            }

        if not partner_data:
            return Response(
                {"detail": "partner data is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            partner = PartnerService.create_partner(
                partner_data,
                created_by=created_by
            )

            roles = []
            for role_data in data.get("roles", []):
                roles.append(
                    PartnerService.add_role(
                        partner.id,
                        role_data,
                        created_by=created_by
                    )
                )

            addresses = []
            for address_data in data.get("addresses", []):
                addresses.append(
                    PartnerService.add_address(
                        partner.id,
                        address_data,
                        created_by=created_by
                    )
                )

            contacts = []
            for contact_data in data.get("contacts", []):
                contacts.append(
                    PartnerService.add_contact(
                        partner.id,
                        contact_data,
                        created_by=created_by
                    )
                )

            identifications = []
            for identification_data in data.get("identifications", []):
                identifications.append(
                    PartnerService.add_identification(
                        partner.id,
                        identification_data,
                        created_by=created_by
                    )
                )

            registrations = []
            for registration_data in data.get("registrations", []):
                registrations.append(
                    PartnerService.add_registration(
                        partner.id,
                        registration_data,
                        created_by=created_by
                    )
                )

            compliance = None
            compliance_data = data.get("compliance_summary")

            if compliance_data:
                compliance_serializer = PartnerComplianceSummarySerializer(
                    data={
                        **compliance_data,
                        "partner": partner.id,
                        "created_by": created_by,
                    }
                )

                compliance_serializer.is_valid(raise_exception=True)
                compliance = compliance_serializer.save()

            return Response(
                {
                    "partner": PartnerSerializer(partner).data,
                    "roles": PartnerRoleSerializer(
                        roles, many=True
                    ).data,
                    "addresses": PartnerAddressSerializer(
                        addresses, many=True
                    ).data,
                    "contacts": PartnerContactSerializer(
                        contacts, many=True
                    ).data,
                    "identifications": PartnerIdentificationSerializer(
                        identifications, many=True
                    ).data,
                    "registrations": PartnerRegistrationSerializer(
                        registrations, many=True
                    ).data,
                    "compliance_summary": (
                        PartnerComplianceSummarySerializer(compliance).data
                        if compliance else None
                    ),
                },
                status=status.HTTP_201_CREATED
            )
    def update(self, request, *args, **kwargs):
        partner = PartnerService.update_partner(kwargs['pk'], request.data, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    def partial_update(self, request, *args, **kwargs):
        partner = PartnerService.update_partner(kwargs['pk'], request.data, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        partner = PartnerService.activate_partner(pk, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        partner = PartnerService.block_partner(pk, reason=request.data.get('reason'), updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['get', 'post'])
    def roles(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerRoleSerializer(PartnerRole.objects.filter(partner_id=pk), many=True).data)
        role = PartnerService.add_role(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerRoleSerializer(role).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def addresses(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerAddressSerializer(PartnerAddress.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_address(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerAddressSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def contacts(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerContactSerializer(PartnerContact.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_contact(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerContactSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def identifications(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerIdentificationSerializer(PartnerIdentification.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_identification(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerIdentificationSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def registrations(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerRegistrationSerializer(PartnerRegistration.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_registration(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerRegistrationSerializer(obj).data, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=["POST"], url_path="validate-policy")
    def validate_policy(self, request):

        partner = Partner.objects.get(
            id=request.data["partner_id"]
        )

        result = PolicyCheckService.validate_partner_action(
            partner=partner,
            action=request.data["action"],
            role=request.data.get("role"),
            context=request.data.get("context")
        )

        return Response(result)
    

    @action(
        detail=False,
        methods=["POST"],   
        url_path="check-role-conflict"
    )
    def check_role_conflict(self, request):

        partner_id = request.data.get("partner_id")
        new_role = request.data.get("new_role")
        # existing_roles = request.data.get("existing_roles", [])

        result = RoleConflictService.validate_role_change(
            partner_id=partner_id,
            new_role=new_role,
            # existing_roles=existing_roles
        )

        return Response(result)
    
    @action(
    detail=False,
    methods=["POST"],
    url_path="validate-usage",
    )
    def validate_usage(self, request):

        partner_id = request.data.get("partner_id")

        partner = Partner.objects.get(
            id=partner_id
        )

        result = PartnerService.validate_usage(
            partner
        )

        return Response(result)
    
    @action(
    detail=True,
    methods=["get"],
    url_path="summary",
    )
    def summary(
        self,
        request,
        pk=None,
    ):
        partner = self.get_object()

        serializer = PartnerSummarySerializer(
            partner
        )

        return Response(
            serializer.data
        )