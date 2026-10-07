# # """
# # BizSoft ERP - ERP Organization

# # Company: Business Information Systems Ltd. / BizSoft
# # Author: Business Information Systems Ltd. / BizSoft
# # Package: erp_organization
# # Version: 1.0.0

# # Purpose:
# # This file is part of the erp_organization ERP business foundation package.

# # Important:
# # - This package defines legal entities, branches, departments, SBUs, facilities,
# #   warehouses, projects, cost centers, profit centers, physical locations,
# #   custodians, and flexible organization relationships.
# # - Organization tells where and who.
# # - Dimension tells how to classify, summarize, analyze, and report.
# # - Do not implement accounting posting, inventory movement, FAR depreciation,
# #   payroll, workflow routing, permission engine, audit trail, or notifications.
# # - core_* packages must not depend on erp_organization.

# # Rule:
# # Selectors read data.
# # Domain Policies validate domain truth.
# # Application Policies validate whether an action is allowed in context.
# # Application Services orchestrate use cases.

# # File Purpose:
# # Orchestrates physical location creation.
# # """

# # from django.db import transaction
# # from erp_organization.constants import OrganizationUnitType, PhysicalLocationType
# # from erp_organization.models import *
# # from erp_organization.validators.organization_validator import BusinessValidationError, NotFoundError, OrganizationValidator
# # from erp_organization.repositories.physical_location_repository import PhysicalLocationRepository


# # # class PhysicalLocationApplicationService:
# # #     @staticmethod
# # #     @transaction.atomic
# # #     def create_physical_location(user=None,data=None):
# # #         data=data or {}; OrganizationValidator.validate_code_format(data.get('location_code'),'location_code')
# # #         branch=OrganizationUnit.objects.filter(unit_code=data.get('responsible_branch_code'),unit_type=OrganizationUnitType.BRANCH).first() if data.get('responsible_branch_code') else data.get('responsible_branch')
# # #         dept=OrganizationUnit.objects.filter(unit_code=data.get('responsible_department_code'),unit_type=OrganizationUnitType.DEPARTMENT).first() if data.get('responsible_department_code') else data.get('responsible_department')
# # #         legal=branch.legal_entity if branch else (dept.legal_entity if dept else None)
# # #         OrganizationValidator.validate_physical_location_responsibility({**data, 'responsible_branch': branch, 'responsible_department': dept})
# # #         unit=OrganizationUnit.objects.create(unit_code=data['location_code'],unit_name=data.get('location_name',data['location_code']),unit_type=OrganizationUnitType.PHYSICAL_LOCATION,legal_entity=legal,parent_unit=branch or dept,created_by=getattr(user,'username',None),is_asset_assignable=data.get('is_asset_assignable',False),is_inventory_storable=data.get('is_inventory_storable',False))
# # #         return PhysicalLocationProfile.objects.create(organization_unit=unit,location_code=data['location_code'],location_name=data.get('location_name',data['location_code']),location_type=data.get('location_type',PhysicalLocationType.OTHER),legal_entity=legal,responsible_branch=branch,responsible_department=dept,address=data.get('address',''),is_internal=data.get('is_internal',True),is_asset_assignable=data.get('is_asset_assignable',False),is_inventory_storable=data.get('is_inventory_storable',False))

# # class PhysicalLocationApplicationService:
# #     repository = PhysicalLocationRepository()
# #     @classmethod
# #     def get_filtered_physical_locations(
# #         cls,
# #         filters
# #     ):
# #         return cls.repository.get_filtered_physical_locations(filters)

# #     @staticmethod
# #     @transaction.atomic
# #     def create_physical_location(user=None, data=None):

# #         data = data or {}
# #         OrganizationValidator.validate_code_format(
# #             data.get("location_code"),
# #             "location_code",
# #         )
# #         responsible_branch = data.get(
# #             "responsible_branch"
# #         )

# #         branch = None

# #         if responsible_branch:

# #             branch = (
# #                 responsible_branch.organization_unit
# #             )

# #         responsible_department = data.get(
# #             "responsible_department"
# #         )

# #         dept = None

# #         if responsible_department:

# #             dept = (
# #                 responsible_department.organization_unit
# #             )

# #         legal = (
# #             branch.legal_entity
# #             if branch
# #             else dept.legal_entity
# #             if dept
# #             else None
# #         )
# #         OrganizationValidator.validate_physical_location_responsibility(
# #             {
# #                 **data,
# #                 "responsible_branch": branch,
# #                 "responsible_department": dept,
# #             }
# #         )
# #         legal_entity_id = data.get("legal_entity")
        
# #         if not legal_entity_id:
# #             raise NotFoundError(
# #                 "Legal entity is required."
# #             )

# #         legal_entity_profile = (
# #             LegalEntityProfile.objects.filter(
# #                 pk=legal_entity_id,
# #                 is_active=True
# #             ).first()
# #         )

# #         if not legal_entity_profile:

# #             raise NotFoundError(
# #                 "Legal entity not found."
# #             )

# #         legal_entity_unit = (
# #             legal_entity_profile.organization_unit
# #         )
# #         parent_unit = branch or dept

# #         unit = OrganizationUnit.objects.create(

# #             unit_code=data["location_code"],

# #             unit_name=data.get(
# #                 "location_name",
# #                 data["location_code"],
# #             ),

# #             unit_type=OrganizationUnitType.PHYSICAL_LOCATION,

# #             legal_entity=legal_entity_unit,

# #             parent_unit=parent_unit,

# #             created_by=getattr(
# #                 user,
# #                 "username",
# #                 None,
# #             ),

# #             is_asset_assignable=data.get(
# #                 "is_asset_assignable",
# #                 False,
# #             ),

# #             is_inventory_storable=data.get(
# #                 "is_inventory_storable",
# #                 False,
# #             ),
# #         )
# #         return PhysicalLocationProfile.objects.create(

# #             organization_unit=unit,

# #             location_code=data["location_code"],

# #             location_name=data.get(
# #                 "location_name",
# #                 data["location_code"],
# #             ),

# #             location_type=data.get(
# #                 "location_type",
# #                 PhysicalLocationType.OTHER,
# #             ),

# #             legal_entity=legal_entity_profile,

# #             responsible_branch=responsible_branch,

# #             responsible_department=responsible_department,

# #             address=data.get(
# #                 "address",
# #                 "",
# #             ),

# #             is_internal=data.get(
# #                 "is_internal",
# #                 True,
# #             ),

# #             is_asset_assignable=data.get(
# #                 "is_asset_assignable",
# #                 False,
# #             ),

# #             is_inventory_storable=data.get(
# #                 "is_inventory_storable",
# #                 False,
# #             ),
# #             is_active=data.get(
# #                 "is_active",
# #                 True
# #             ),
# #         )

# """
# BizSoft ERP - ERP Organization

# Company: Business Information Systems Ltd. / BizSoft
# Author: Business Information Systems Ltd. / BizSoft
# Package: erp_organization
# Version: 1.0.0

# Purpose:
# This file is part of the erp_organization ERP business foundation package.

# Important:
# - This package defines legal entities, branches, departments, SBUs, facilities,
#   warehouses, projects, cost centers, profit centers, physical locations,
#   custodians, and flexible organization relationships.
# - Organization tells where and who.
# - Dimension tells how to classify, summarize, analyze, and report.
# - Do not implement accounting posting, inventory movement, FAR depreciation,
#   payroll, workflow routing, permission engine, audit trail, or notifications.
# - core_* packages must not depend on erp_organization.

# Rule:
# Selectors read data.
# Domain Policies validate domain truth.
# Application Policies validate whether an action is allowed in context.
# Application Services orchestrate use cases.

# File Purpose:
# Orchestrates physical location creation.
# """

# from django.db import transaction
# from erp_organization.constants import OrganizationUnitType, PhysicalLocationType
# from erp_organization.models import *
# from erp_organization.validators.organization_validator import BusinessValidationError, NotFoundError, OrganizationValidator
# from erp_organization.repositories.physical_location_repository import PhysicalLocationRepository


# class PhysicalLocationApplicationService:
#     @staticmethod
#     @transaction.atomic
#     def create_physical_location(user=None, data=None):

#         data = data or {}

        
#         location_code = data.get("location_code")

#         OrganizationValidator.validate_code_format(
#             location_code,
#             "location_code",
#         )

    
#         legal_entity_id = data.get("legal_entity")

#         if not legal_entity_id:
#             raise NotFoundError(
#                 "Legal entity is required."
#             )

#         legal_entity_profile = (
#             LegalEntityProfile.objects
#             .filter(
#                 pk=legal_entity_id,
#                 is_active=True,
#             )
#             .first()
#         )

#         if not legal_entity_profile:
#             raise NotFoundError(
#                 "Legal entity not found."
#             )

#         legal_entity_unit = (
#             legal_entity_profile.organization_unit
#         )

    
#         responsible_branch_id = data.get(
#             "responsible_branch"
#         )

#         responsible_branch = None
#         branch_unit = None

#         if responsible_branch_id is not None:

#             responsible_branch = (
#                 BranchProfile.objects
#                 .filter(
#                     pk=responsible_branch_id,
#                     is_active=True,
#                 )
#                 .first()
#             )

#             if not responsible_branch:
#                 raise NotFoundError(
#                     "Responsible branch not found."
#                 )

#             branch_unit = (
#                 responsible_branch.organization_unit
#             )

#             # Branch must belong to selected legal entity
#             if (
#                 responsible_branch.legal_entity_id
#                 != legal_entity_profile.id
#             ):
#                 raise BusinessValidationError(
#                     "Responsible branch does not belong to selected legal entity."
#                 )


#         responsible_department_id = data.get(
#             "responsible_department"
#         )

#         responsible_department = None
#         department_unit = None

#         if responsible_department_id is not None:

#             responsible_department = (
#                 DepartmentProfile.objects
#                 .filter(
#                     pk=responsible_department_id,
#                     is_active=True,
#                 )
#                 .first()
#             )

#             if not responsible_department:
#                 raise NotFoundError(
#                     "Responsible department not found."
#                 )

#             department_unit = (
#                 responsible_department.organization_unit
#             )

#             if (
#                 responsible_department.legal_entity_id
#                 != legal_entity_profile.id
#             ):
#                 raise BusinessValidationError(
#                     "Responsible department does not belong to selected legal entity."
#                 )


#         OrganizationValidator.validate_physical_location_responsibility(
#             {
#                 **data,
#                 "responsible_branch": responsible_branch,
#                 "responsible_department": responsible_department,
#             }
#         )

    
#         parent_unit = (
#             department_unit
#             or branch_unit
#             or legal_entity_unit
#         )


#         unit = OrganizationUnit.objects.create(

#             unit_code=location_code,

#             unit_name=data.get(
#                 "location_name",
#                 location_code,
#             ),

#             unit_type=OrganizationUnitType.PHYSICAL_LOCATION,

#             legal_entity=legal_entity_unit,

#             parent_unit=parent_unit,

#             created_by=getattr(
#                 user,
#                 "username",
#                 None,
#             ),

#             is_asset_assignable=data.get(
#                 "is_asset_assignable",
#                 False,
#             ),

#             is_inventory_storable=data.get(
#                 "is_inventory_storable",
#                 False,
#             ),

#             is_active=data.get(
#                 "is_active",
#                 True,
#             ),

#             effective_from=data.get(
#                 "effective_from"
#             ),

#             effective_to=data.get(
#                 "effective_to"
#             ),
#         )

    
#         physical_location = (
#             PhysicalLocationProfile.objects.create(

#                 organization_unit=unit,

#                 location_code=location_code,

#                 location_name=data.get(
#                     "location_name",
#                     location_code,
#                 ),

#                 location_type=data.get(
#                     "location_type",
#                     PhysicalLocationType.OTHER,
#                 ),

#                 legal_entity=legal_entity_unit,

#                 responsible_branch=responsible_branch,

#                 responsible_department=responsible_department,

#                 address=data.get(
#                     "address",
#                     "",
#                 ),

#                 is_internal=data.get(
#                     "is_internal",
#                     True,
#                 ),

#                 is_asset_assignable=data.get(
#                     "is_asset_assignable",
#                     False,
#                 ),

#                 is_inventory_storable=data.get(
#                     "is_inventory_storable",
#                     False,
#                 ),

#                 is_active=data.get(
#                     "is_active",
#                     True,
#                 ),
#             )
#         )

#         return PhysicalLocationProfile.objects.create(

#             organization_unit=unit,

#             location_code=data["location_code"],

#             location_name=data.get(
#                 "location_name",
#                 data["location_code"],
#             ),

#             location_type=data.get(
#                 "location_type",
#                 PhysicalLocationType.OTHER,
#             ),

#             legal_entity=legal_entity_unit,

#             responsible_branch=responsible_branch,

#             responsible_department=responsible_department,

#             # address=data.get(
#             #     "address",
#             #     "",
#             # ),
#             address=data.get("address") or "",

#             is_internal=data.get(
#                 "is_internal",
#                 True,
#             ),

#             is_asset_assignable=data.get(
#                 "is_asset_assignable",
#                 False,
#             ),

#             is_inventory_storable=data.get(
#                 "is_inventory_storable",
#                 False,
#             ),
#             is_active=data.get(
#                 "is_active",
#                 True
#             ),
#         )

from django.db import transaction

from erp_organization.constants import (
    OrganizationUnitType,
    PhysicalLocationType,
)

from erp_organization.models import *

from erp_organization.validators.organization_validator import (
    BusinessValidationError,
    NotFoundError,
    OrganizationValidator,
)

from erp_organization.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)


class PhysicalLocationApplicationService:

    @staticmethod
    @transaction.atomic
    def create_physical_location(user=None, data=None):

        data = data or {}

        location_code = data.get("location_code")

        OrganizationValidator.validate_code_format(
            location_code,
            "location_code",
        )


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

        responsible_branch_id = data.get(
            "responsible_branch"
        )

        responsible_branch = None
        branch_unit = None

        if responsible_branch_id is not None:

            responsible_branch = (
                BranchProfile.objects
                .filter(
                    pk=responsible_branch_id,
                    is_active=True,
                )
                .first()
            )

            if not responsible_branch:
                raise NotFoundError(
                    "Responsible branch not found."
                )

            branch_unit = (
                responsible_branch.organization_unit
            )

            if (
                responsible_branch.legal_entity_id
                != legal_entity_profile.id
            ):
                raise BusinessValidationError(
                    "Responsible branch does not belong to selected legal entity."
                )

 
        responsible_department_id = data.get(
            "responsible_department"
        )

        responsible_department = None
        department_unit = None

        if responsible_department_id is not None:

            responsible_department = (
                DepartmentProfile.objects
                .filter(
                    pk=responsible_department_id,
                    is_active=True,
                )
                .first()
            )

            if not responsible_department:
                raise NotFoundError(
                    "Responsible department not found."
                )

            department_unit = (
                responsible_department.organization_unit
            )

            if (
                responsible_department.legal_entity_id
                != legal_entity_profile.id
            ):
                raise BusinessValidationError(
                    "Responsible department does not belong to selected legal entity."
                )


        OrganizationValidator.validate_physical_location_responsibility(
            {
                **data,
                "responsible_branch": responsible_branch,
                "responsible_department": responsible_department,
            }
        )

        parent_unit = (
            department_unit
            or branch_unit
            or legal_entity_unit
        )

   
        unit = OrganizationUnit.objects.create(

            unit_code=location_code,

            unit_name=data.get(
                "location_name",
                location_code,
            ),

            unit_type=OrganizationUnitType.PHYSICAL_LOCATION,

            legal_entity=legal_entity_unit,

            parent_unit=parent_unit,

            created_by=getattr(
                user,
                "username",
                None,
            ),

            is_asset_assignable=data.get(
                "is_asset_assignable",
                False,
            ),

            is_inventory_storable=data.get(
                "is_inventory_storable",
                False,
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
        )

    
        physical_location = (
            PhysicalLocationProfile.objects.create(

                organization_unit=unit,

                location_code=location_code,

                location_name=data.get(
                    "location_name",
                    location_code,
                ),

                location_type=data.get(
                    "location_type",
                    PhysicalLocationType.OTHER,
                ),

                legal_entity=legal_entity_unit,

                responsible_branch=responsible_branch,

                responsible_department=responsible_department,

                address=data.get("address") or "",

                is_internal=data.get(
                    "is_internal",
                    True,
                ),

                is_asset_assignable=data.get(
                    "is_asset_assignable",
                    False,
                ),

                is_inventory_storable=data.get(
                    "is_inventory_storable",
                    False,
                ),

                is_active=data.get(
                    "is_active",
                    True,
                ),
            )
        )

      

        return physical_location