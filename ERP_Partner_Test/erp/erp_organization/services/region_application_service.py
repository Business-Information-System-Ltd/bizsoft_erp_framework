"""Application service for Region master data."""

from django.db import transaction

from erp_organization.models import Region

from erp_organization.repositories.region_repository import RegionRepository

from erp_organization.validators.organization_validator import (
    OrganizationValidator,
    NotFoundError,
)


class RegionApplicationService:

    repository = RegionRepository()

    @classmethod
    def get_filtered_regions(cls, filters=None):
        return cls.repository.get_filtered_regions(filters)

    @staticmethod
    @transaction.atomic
    def create_region(data=None):

        data = data or {}

        code = data.get("region_code")

        OrganizationValidator.validate_code_format(
            code,
            "region_code",
        )

        timezone_name = data.get("timezone_name")

        if not timezone_name:
            raise ValueError(
                "timezone_name is required."
            )

        return Region.objects.create(
            region_code=code,
            region_name=data.get(
                "region_name",
                code,
            ),
            timezone_name=timezone_name,
            is_active=data.get(
                "is_active",
                True,
            ),
            map_latitude=data.get("map_latitude"),
            map_longitude=data.get("map_longitude"),
        )

    @staticmethod
    @transaction.atomic
    def update_region(region_id, data=None):

        region = Region.objects.filter(
            pk=region_id
        ).first()

        if not region:
            raise NotFoundError(
                "Region not found."
            )

        data = data or {}

        if "region_code" in data:

            OrganizationValidator.validate_code_format(
                data["region_code"],
                "region_code",
            )

            region.region_code = data["region_code"]

        if "region_name" in data:
            region.region_name = data["region_name"]

        if "timezone_name" in data:
            timezone_name = data["timezone_name"]

            if not timezone_name:
                raise ValueError(
                    "timezone_name cannot be empty."
                )

            region.timezone_name = timezone_name

        if "is_active" in data:
            region.is_active = data["is_active"]

        if "map_latitude" in data:
            region.map_latitude = data["map_latitude"]

        
        if "map_longitude" in data:
            region.map_longitude = data["map_longitude"]

        region.save()

        return region