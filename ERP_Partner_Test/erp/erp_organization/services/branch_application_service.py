"""
BizSoft ERP - ERP Organization

Company: Business Information Systems Ltd. / BizSoft
Author: Business Information Systems Ltd. / BizSoft
Package: erp_organization
Version: 1.0.0

Purpose:
This file is part of the erp_organization ERP business foundation package.

Important:
- This package defines legal entities, branches, departments, SBUs, facilities,
  warehouses, projects, cost centers, profit centers, physical locations,
  custodians, and flexible organization relationships.
- Organization tells where and who.
- Dimension tells how to classify, summarize, analyze, and report.
- Do not implement accounting posting, inventory movement, FAR depreciation,
  payroll, workflow routing, permission engine, audit trail, or notifications.
- core_* packages must not depend on erp_organization.

Rule:
Selectors read data.
Domain Policies validate domain truth.
Application Policies validate whether an action is allowed in context.
Application Services orchestrate use cases.

File Purpose:
Orchestrates branch creation.
"""

from django.db import transaction
from erp_organization.constants import OrganizationUnitType, PhysicalLocationType
from erp_organization.models import *
from erp_organization.validators.organization_validator import BusinessValidationError, NotFoundError, OrganizationValidator
from erp_organization.repositories.branch_repository import BranchRepository

from erp_organization.application_policies.branch_application_policy import BranchApplicationPolicyService


class BranchApplicationService:
    repository = BranchRepository()
    @classmethod
    def get_filtered_branches(
        cls,
        filters
    ):
        return cls.repository.get_filtered_branches(filters)

    @staticmethod
    @transaction.atomic
    def create_branch(user=None, data=None):

        data = data or {}

        branch_code = data.get(
            "branch_code"
        )

        OrganizationValidator.validate_code_format(
            branch_code,
            "branch_code",
        )

       
        legal_entity_id = data.get("legal_entity")

        if not legal_entity_id:
            raise NotFoundError(
                "Legal entity is required."
            )

        legal_entity_profile = (
            LegalEntityProfile.objects.filter(
                pk=legal_entity_id,
                is_active=True
            ).first()
        )

        if not legal_entity_profile:

            raise NotFoundError(
                "Legal entity not found."
            )

        legal_entity_unit = (
            legal_entity_profile.organization_unit
        )

        is_active = data.get(
                    "is_active",
                    True,
                )

        # region = (
        #     Region.objects
        #     .filter(
        #         pk=data.get("region"),
        #         is_active=True,
        #     )
        #     .first()
        # )

        # if not region:
        #     raise NotFoundError(
        #         "Region not found."
        #     )

        # zone = (
        #     Zone.objects
        #     .filter(
        #         pk=data.get("zone"),
        #         is_active=True,
        #     )
        #     .first()
        # )

        # if not zone:
        #     raise NotFoundError(
        #         "Zone not found."
        #     )
        # if zone.region_id != region.id:
        #     raise BusinessValidationError(
        #         "Selected zone does not belong to selected region."
        #     )

        # address = (
        #     Address.objects
        #     .filter(
        #         pk=data.get("address"),
        #         is_active=True,
        #     )
        #     .first()
        # )

        # if not address:
        #     raise NotFoundError(
        #         "Address not found."
        #     )
        # if address.region_id != region.id:
        #     raise BusinessValidationError(
        #         "Selected address does not belong to selected region."
        #     )

        # if address.zone_id != zone.id:
        #     raise BusinessValidationError(
        #         "Selected address does not belong to selected zone."
        #     )

        region_id = data.get("region")
        zone_id = data.get("zone")
        address_id = data.get("address")

        region = None
        zone = None
        address = None


        
        if region_id is not None:
            region = (
                Region.objects
                .filter(
                    pk=region_id,
                    is_active=True,
                )
                .first()
            )

            if not region:
                raise NotFoundError(
                    "Region not found."
                )



        if zone_id is not None:
            zone = (
                Zone.objects
                .filter(
                    pk=zone_id,
                    is_active=True,
                )
                .first()
            )

            if not zone:
                raise NotFoundError(
                    "Zone not found."
                )

            if region is None:
                raise BusinessValidationError(
                    "Region is required when zone is provided."
                )

            if zone.region_id != region.id:
                raise BusinessValidationError(
                    "Selected zone does not belong to selected region."
                )



        if address_id is not None:
            address = (
                Address.objects
                .filter(
                    pk=address_id,
                    is_active=True,
                )
                .first()
            )

            if not address:
                raise NotFoundError(
                    "Address not found."
                )

            if region is None:
                raise BusinessValidationError(
                    "Region is required when address is provided."
                )

            if address.region_id != region.id:
                raise BusinessValidationError(
                    "Selected address does not belong to selected region."
                )

            if zone is None:
                raise BusinessValidationError(
                    "Zone is required when address is provided."
                )

            if address.zone_id != zone.id:
                raise BusinessValidationError(
                    "Selected address does not belong to selected zone."
                )
        branch_unit = OrganizationUnit.objects.create(

            unit_code=branch_code,

            unit_name=data.get(
                "branch_name",
                branch_code,
            ),

            unit_type=OrganizationUnitType.BRANCH,

            legal_entity=legal_entity_unit,

            parent_unit=legal_entity_unit,
            is_cost_center=data.get(
                "is_cost_center",
                False,
            ),

            is_profit_center=data.get(
                "is_profit_center",
                False,
            ),

            is_inventory_storable=data.get(
                "is_inventory_storable",
                False,
            ),

            is_asset_assignable=data.get(
                "is_asset_assignable",
                False,
            ),
            is_active=is_active,

            status=(
                UnitStatus.ACTIVE
                if is_active
                else UnitStatus.INACTIVE
            ),
            effective_from=data.get(
                "effective_from"
            ),

            effective_to=data.get(
                "effective_to"
            ),

            created_by=getattr(
                user,
                "username",
                None,
            ),
        )

        branch = BranchProfile.objects.create(

            organization_unit=branch_unit,

            branch_code=branch_code,

            branch_name=data.get(
                "branch_name",
                branch_code,
            ),

            legal_entity=legal_entity_profile,

            branch_type=data.get(
                "branch_type",
                "",
            ),

            

            region=region,

            zone=zone,

            address=address,

            latitude=data.get("latitude"),

            longitude=data.get("longitude"),

            is_head_office=data.get(
                "is_head_office",
                False,
            ),

            is_bank_branch=data.get(
                "is_bank_branch",
                False,
            ),
            is_active=data.get(
                "is_active",
                True
            ),
        )

        return branch
    @staticmethod
    @transaction.atomic
    def update_branch(
        branch_id,
        user=None,
        data=None,
    ):
        data = data or {}

        branch = (
            BranchProfile.objects
            .select_related(
                "organization_unit",
                "legal_entity",
            )
            .filter(pk=branch_id)
            .first()
        )

        if not branch:
            raise NotFoundError(
                "Branch not found."
            )

        branch_code = data.get(
            "branch_code",
            branch.branch_code,
        )

        branch_name = data.get(
            "branch_name",
            branch.branch_name,
        )

        OrganizationValidator.validate_code_format(
            branch_code,
            "branch_code",
        )

        legal_entity_id = data.get(
            "legal_entity",
            branch.legal_entity_id,
        )

        legal_entity_profile = (
            LegalEntityProfile.objects
            .select_related("organization_unit")
            .filter(
                pk=legal_entity_id,
                is_active=True,
            )
            .first()
        )

        if not legal_entity_profile:
            raise NotFoundError(
                "Legal entity not found."
            )

        legal_entity_unit = (
            legal_entity_profile.organization_unit
        )

        region = (
            Region.objects
            .filter(
                pk=data.get(
                    "region",
                    branch.region_id,
                ),
                is_active=True,
            )
            .first()
        )
        zone = (
            Zone.objects
            .filter(
                pk=data.get(
                    "zone",
                    branch.zone_id,
                ),
                is_active=True,
            )
            .first()
        )

        address = (
            Address.objects
            .filter(
                pk=data.get(
                    "address",
                    branch.address_id,
                ),
                is_active=True,
            )
            .first()
        )
        organization_unit = (
            branch.organization_unit
        )
        is_active = data.get(
            "is_active",
            branch.is_active,
        )
        organization_unit.unit_code = (
            branch_code
        )

        organization_unit.unit_name = (
            branch_name
        )

        organization_unit.unit_type = (
            OrganizationUnitType.BRANCH
        )

        organization_unit.legal_entity = (
            legal_entity_unit
        )

        organization_unit.parent_unit = (
            legal_entity_unit
        )

        organization_unit.is_cost_center = data.get(
            "is_cost_center",
            organization_unit.is_cost_center,
        )

        organization_unit.is_profit_center = data.get(
            "is_profit_center",
            organization_unit.is_profit_center,
        )

        organization_unit.is_inventory_storable = data.get(
            "is_inventory_storable",
            organization_unit.is_inventory_storable,
        )

        organization_unit.is_asset_assignable = data.get(
            "is_asset_assignable",
            organization_unit.is_asset_assignable,
        )

        organization_unit.is_active = (
            is_active
        )

        organization_unit.status = (
            UnitStatus.ACTIVE
            if is_active
            else UnitStatus.INACTIVE
        )
        if "effective_from" in data:
            organization_unit.effective_from = (
                data.get("effective_from")
            )

        if "effective_to" in data:
            organization_unit.effective_to = (
                data.get("effective_to")
            )

        organization_unit.updated_by = getattr(
            user,
            "username",
            None,
        )

        organization_unit.save()
        branch.branch_code = branch_code

        branch.branch_name = branch_name

        branch.legal_entity = (
            legal_entity_profile
        )

        if "branch_type" in data:
            branch.branch_type = data.get(
                "branch_type"
            )

        branch.region =(region)
        branch.zone =(zone)
        branch.address =(address)

        if "latitude" in data:
            branch.latitude = data.get("latitude")

        if "longitude" in data:
            branch.longitude = data.get("longitude")

        if "is_head_office" in data:
            branch.is_head_office = data.get(
                "is_head_office"
            )

        if "is_bank_branch" in data:
            branch.is_bank_branch = data.get(
                "is_bank_branch"
            )

        branch.is_active = is_active

        branch.save()

        return branch