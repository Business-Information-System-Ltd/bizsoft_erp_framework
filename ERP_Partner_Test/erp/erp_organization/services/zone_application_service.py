"""Application service for Zone master data."""
from django.db import transaction
from erp_organization.models import Zone, Region
from erp_organization.repositories.zone_repository import ZoneRepository
from erp_organization.validators.organization_validator import OrganizationValidator, NotFoundError
class ZoneApplicationService:
    repository=ZoneRepository()
    @classmethod
    def get_filtered_zones(cls, filters=None): return cls.repository.get_filtered_zones(filters)
    @staticmethod
    @transaction.atomic
    def create_zone(data=None):
        data=data or {}; code=data.get("zone_code"); OrganizationValidator.validate_code_format(code,"zone_code")
        region=Region.objects.filter(pk=data.get("region"),is_active=True).first()
        if not region: raise NotFoundError("Region not found.")
        return Zone.objects.create(zone_code=code,zone_name=data.get("zone_name",code),region=region,is_active=data.get("is_active",True))
    @staticmethod
    @transaction.atomic
    def update_zone(zone_id,data=None):
        zone=Zone.objects.select_related("region").filter(pk=zone_id).first()
        if not zone: raise NotFoundError("Zone not found.")
        data=data or {}
        if "zone_code" in data: OrganizationValidator.validate_code_format(data["zone_code"],"zone_code"); zone.zone_code=data["zone_code"]
        if "zone_name" in data: zone.zone_name=data["zone_name"]
        if "region" in data:
            region=Region.objects.filter(pk=data["region"],is_active=True).first()
            if not region: raise NotFoundError("Region not found.")
            zone.region=region
        if "is_active" in data: zone.is_active=data["is_active"]
        zone.save(); return zone
