"""Application service for Address master data."""
from django.db import transaction
from erp_organization.models import Address, Region, Zone
from erp_organization.repositories.address_repository import AddressRepository
from erp_organization.validators.organization_validator import NotFoundError, BusinessValidationError
class AddressApplicationService:
    repository=AddressRepository()
    @classmethod
    def get_filtered_addresses(cls, filters=None): return cls.repository.get_filtered_addresses(filters)
    @staticmethod
    def _resolve(data, instance=None):
        region_id=data.get("region", instance.region_id if instance else None); zone_id=data.get("zone", instance.zone_id if instance else None)
        region=Region.objects.filter(pk=region_id,is_active=True).first()
        if not region: raise NotFoundError("Region not found.")
        zone=Zone.objects.filter(pk=zone_id,is_active=True).first()
        if not zone: raise NotFoundError("Zone not found.")
        if zone.region_id != region.id: raise BusinessValidationError("Selected zone does not belong to selected region.")
        return region,zone
    @staticmethod
    @transaction.atomic
    def create_address(data=None):
        data=data or {}; region,zone=AddressApplicationService._resolve(data)
        return Address.objects.create(address_line_1=data.get("address_line_1",""),address_line_2=data.get("address_line_2"),township=data.get("township",""),city=data.get("city",""),region=region,zone=zone,postal_code=data.get("postal_code"),is_active=data.get("is_active",True))
    @staticmethod
    @transaction.atomic
    def update_address(address_id,data=None):
        address=Address.objects.filter(pk=address_id).first()
        if not address: raise NotFoundError("Address not found.")
        data=data or {}; region,zone=AddressApplicationService._resolve(data,address)
        for field in ("address_line_1","address_line_2","township","city","postal_code","is_active"):
            if field in data: setattr(address,field,data[field])
        address.region=region; address.zone=zone; address.save(); return address
