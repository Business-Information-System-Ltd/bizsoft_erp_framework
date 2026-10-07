"""
BizSoft ERP - Partners Module

File:
    erp_partners/services/partner_service.py

Purpose:
    Provides transaction-safe partner application service methods.

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


from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import NotFound, ValidationError
from erp_partners.services.role_conflict_service import RoleConflictService
from erp_partners.services.relationship_service import (
    RelationshipService
)
from erp_partners.enums.partner_enums import PartnerStatus
from erp_partners.models import PartnerAddress, PartnerContact, PartnerIdentification, PartnerRegistration, PartnerRole, PartnerRelationship, Partner, PartnerComplianceSummary
from erp_partners.serializers.partner_compliance_serializers import (
    PartnerComplianceSummarySerializer,
)
from erp_partners.repositories.partner_repository import PartnerRepository
from erp_partners.serializers import (
    PartnerAddressSerializer,
    PartnerContactSerializer,
    PartnerIdentificationSerializer,
    PartnerRegistrationSerializer,
    PartnerRoleSerializer,
    PartnerSerializer,
)
from erp_partners.services.role_conflict_service import (
    RoleConflictService
)


class PartnerService:
    repository = PartnerRepository()

    @classmethod
    @transaction.atomic
    def create_partner(cls, data, created_by=None):
        """Create a partner after serializer validation."""
        serializer = PartnerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)
        payload['created_by'] = created_by
        return cls.repository.create(payload)

    @classmethod
    @transaction.atomic
    def update_partner(cls, partner_id, data, updated_by=None):
        """Update a partner after serializer validation."""
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        serializer = PartnerSerializer(partner, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)
        payload['updated_by'] = updated_by
        return cls.repository.update(partner, payload)

    @classmethod
    @transaction.atomic
    def activate_partner(cls, partner_id, updated_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        partner.status = PartnerStatus.ACTIVE
        partner.is_active = True
        partner.updated_by = updated_by
        partner.save(update_fields=['status', 'is_active', 'updated_by', 'updated_at'])
        return partner

    @classmethod
    @transaction.atomic
    def block_partner(cls, partner_id, reason=None, updated_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        partner.status = PartnerStatus.BLOCKED
        partner.updated_by = updated_by
        if reason:
            partner.remarks = reason
        partner.save(update_fields=['status', 'updated_by', 'remarks', 'updated_at'])
        return partner

    @classmethod
    @transaction.atomic
    def add_role(cls, partner_id, role_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)

        if not partner:
            raise NotFound("Partner not found.")

        # Check role conflict before creating the role
        conflict_result = RoleConflictService.validate_role_change(
            partner_id=partner.id,
            new_role=role_data.get("role_type"),
        )

        if not conflict_result["allowed"]:
            raise ValidationError({
                "role_type": conflict_result["message"]
            })

        # payload = {
        #     **role_data,
        #     "partner": partner.id,
        #     "created_by": created_by,
        # }

        # serializer = PartnerRoleSerializer(data=payload)
        # serializer.is_valid(raise_exception=True)

        # return PartnerRole.objects.create(
        #     **serializer.validated_data
        # )

        serializer = PartnerRoleSerializer(
            data=role_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return PartnerRole.objects.create(
            partner=partner,
            created_by=created_by,
            **serializer.validated_data
        )
    # @classmethod
    # @transaction.atomic
    # def add_address(cls, partner_id, address_data, created_by=None):
    #     partner = cls.repository.get_by_id(partner_id)
    #     if not partner:
    #         raise NotFound('Partner not found.')
    #     # payload = {**address_data, 'partner': partner.id, 'created_by': created_by}
        
    #     serializer = PartnerAddressSerializer(data=payload)
    #     serializer.is_valid(raise_exception=True)
    #     # return PartnerAddress.objects.create(**serializer.validated_data)
    #     payload = serializer.validated_data.copy()

    #     payload["partner"] = partner

    #     if created_by:
    #         payload["created_by"] = created_by

    #     return PartnerAddress.objects.create(
    #         **payload
    #     )

    @classmethod
    @transaction.atomic
    def add_address(cls, partner_id, address_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)

        if not partner:
            raise NotFound("Partner not found.")

        serializer = PartnerAddressSerializer(
            data=address_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return PartnerAddress.objects.create(
            partner=partner,
            created_by=created_by,
            **serializer.validated_data
        )

    @classmethod
    @transaction.atomic
    def add_contact(cls, partner_id, contact_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        # payload = {**contact_data, 'partner': partner.id, 'created_by': created_by}
        # serializer = PartnerContactSerializer(data=payload)
        # serializer.is_valid(raise_exception=True)
        # return PartnerContact.objects.create(**serializer.validated_data)
        serializer = PartnerContactSerializer(
            data=contact_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return PartnerContact.objects.create(
            partner=partner,
            created_by=created_by,
            **serializer.validated_data
        )

    @classmethod
    @transaction.atomic
    def add_identification(cls, partner_id, identification_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        # payload = {**identification_data, 'partner': partner.id, 'created_by': created_by}
        # serializer = PartnerIdentificationSerializer(data=payload)
        # serializer.is_valid(raise_exception=True)
        # return PartnerIdentification.objects.create(**serializer.validated_data)

        serializer = PartnerIdentificationSerializer(
            data=identification_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return PartnerIdentification.objects.create(
            partner=partner,
            created_by=created_by,
            **serializer.validated_data
        )

    @classmethod
    @transaction.atomic
    def add_registration(cls, partner_id, registration_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        # payload = {**registration_data, 'partner': partner.id, 'created_by': created_by}
        # serializer = PartnerRegistrationSerializer(data=payload)
        # serializer.is_valid(raise_exception=True)
        # return PartnerRegistration.objects.create(**serializer.validated_data)
        serializer = PartnerRegistrationSerializer(
            data=registration_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return PartnerRegistration.objects.create(
            partner=partner,
            created_by=created_by,
            **serializer.validated_data
        )
    @classmethod
    def validate_usage(
        cls,
        partner,
        
    ):

        usages = []

        if PartnerRole.objects.filter(
            partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerRole")

        if PartnerRelationship.objects.filter(
            from_partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerRelationship (From)")

        if PartnerRelationship.objects.filter(
            to_partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerRelationship (To)")

        if PartnerAddress.objects.filter(
            partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerAddress")

        if PartnerContact.objects.filter(
            partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerContact")

        if PartnerIdentification.objects.filter(
            partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerIdentification")

        if PartnerRegistration.objects.filter(
            partner=partner,
            is_active=True,
        ).exists():

            usages.append("PartnerRegistration")

        return {
            "can_delete": len(usages) == 0,
            "usages": usages,
        }
    
    @classmethod
    @transaction.atomic
    def create_with_context(
            cls,
            partner_data,
            role_data=None,
            addresses_data=None,
            contacts_data=None,
            identifications_data=None,
            registrations_data=None,
            relationship_data=None,
            compliance_summary_data=None,
            created_by=None
    ):

        partner = cls.create_partner(
            partner_data,
            created_by
        )

        role = None

        if role_data:

            role = cls.add_role(
                partner.id,
                role_data,
                created_by
            )



        addresses = []

        for address_data in addresses_data or []:
            address = cls.add_address(
                partner.id,
                address_data,
                created_by
            )
            addresses.append(address)

        contacts = []

        for contact_data in contacts_data or []:
            contact = cls.add_contact(
                partner.id,
                contact_data,
                created_by
            )
            contacts.append(contact)

        identifications = []

        for identification_data in identifications_data or []:
            identification = cls.add_identification(
                partner.id,
                identification_data,
                created_by
            )
            identifications.append(identification)

        registrations = []

        for registration_data in registrations_data or []:
            registration = cls.add_registration(
                partner.id,
                registration_data,
                created_by
            )
            registrations.append(registration)

        relationship = None

        if relationship_data:

            relationship_data[
                "from_partner"
            ] = partner.id

            relationship = (
                RelationshipService
                .create_relationship(
                    relationship_data,
                    created_by
                )
            )

        compliance_summary = None

        if compliance_summary_data:

            payload = {
                **compliance_summary_data,
                "partner": partner.id,
                "created_by": created_by,
            }

            serializer = PartnerComplianceSummarySerializer(
                data=payload
            )

            serializer.is_valid(
                raise_exception=True
            )

            compliance_summary = (
                PartnerComplianceSummary.objects.create(
                    **serializer.validated_data
                )
            )

        return {
            "partner": partner,
            "role": role,
            "addresses": addresses,
            "contacts": contacts,
            "identifications": identifications,
            "registrations": registrations,
            "relationship": relationship,
            "compliance_summary": compliance_summary,
        }