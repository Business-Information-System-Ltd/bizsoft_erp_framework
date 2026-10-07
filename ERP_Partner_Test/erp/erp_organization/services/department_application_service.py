from django.db import transaction

from erp_organization.constants import OrganizationUnitType
from erp_organization.models import (
    DepartmentProfile,
    LegalEntityProfile,
    OrganizationUnit,
    BranchProfile,
)
from erp_organization.validators.organization_validator import (
    NotFoundError,
    OrganizationValidator,
)
from erp_organization.repositories.department_repository import (
    DepartmentRepository,
)


class DepartmentApplicationService:

    repository = DepartmentRepository()

    @classmethod
    def get_filtered_departments(cls, filters):
        return cls.repository.get_filtered_departments(filters)

    @staticmethod
    @transaction.atomic
    def create_department(user=None, data=None):

        data = data or {}

        # ----------------------------------------
        # Department Code
        # ----------------------------------------
        department_code = data.get("department_code")

        OrganizationValidator.validate_code_format(
            department_code,
            "department_code",
        )

        # ----------------------------------------
        # Legal Entity
        # Request:
        # "legal_entity": 1
        # ----------------------------------------
        legal_entity_id = data.get("legal_entity")

        if not legal_entity_id:
            raise NotFoundError(
                "Legal entity is required."
            )

        legal_entity_profile = (
            LegalEntityProfile.objects
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

        # ----------------------------------------
        # Branch - Optional
        # Request:
        # "branch": 1
        # ----------------------------------------
        branch_id = data.get("branch")

        branch_profile = None
        branch_unit = None

        if branch_id is not None:

            branch_profile = (
                BranchProfile.objects
                .filter(
                    pk=branch_id,
                    is_active=True,
                )
                .first()
            )

            if not branch_profile:
                raise NotFoundError(
                    "Branch not found."
                )

            branch_unit = (
                branch_profile.organization_unit
            )

            # Branch must belong to same legal entity
            if branch_profile.legal_entity_id != legal_entity_profile.id:
                raise NotFoundError(
                    "Selected branch does not belong to selected legal entity."
                )

        # ----------------------------------------
        # Parent Department - Optional
        # Request:
        # "parent_department": 1
        # ----------------------------------------
        parent_department_id = data.get(
            "parent_department"
        )

        parent_department_profile = None
        parent_department_unit = None

        if parent_department_id is not None:

            parent_department_profile = (
                DepartmentProfile.objects
                .filter(
                    pk=parent_department_id,
                    is_active=True,
                )
                .first()
            )

            if not parent_department_profile:
                raise NotFoundError(
                    "Parent department not found."
                )

            parent_department_unit = (
                parent_department_profile.organization_unit
            )

            # Parent department must belong
            # to same legal entity
            if (
                parent_department_profile.legal_entity_id
                != legal_entity_profile.id
            ):
                raise NotFoundError(
                    "Parent department does not belong to selected legal entity."
                )

        # ----------------------------------------
        # Determine Parent Organization Unit
        # ----------------------------------------
        parent_unit = (
            parent_department_unit
            or branch_unit
            or legal_entity_unit
        )

        # ----------------------------------------
        # Create OrganizationUnit
        # ----------------------------------------
        department_unit = OrganizationUnit.objects.create(

            unit_code=department_code,

            unit_name=data.get(
                "department_name",
                department_code,
            ),

            unit_type=OrganizationUnitType.DEPARTMENT,

            legal_entity=legal_entity_unit,

            parent_unit=parent_unit,

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
                True,
            ),

            is_active=data.get(
                "is_active",
                True,
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

        # ----------------------------------------
        # Create DepartmentProfile
        # ----------------------------------------
        department = DepartmentProfile.objects.create(

            organization_unit=department_unit,

            department_code=department_code,

            department_name=data.get(
                "department_name",
                department_code,
            ),

            legal_entity=legal_entity_profile,

            branch=branch_profile,

            parent_department=parent_department_profile,

            is_active=data.get(
                "is_active",
                True,
            ),
        )

        return department