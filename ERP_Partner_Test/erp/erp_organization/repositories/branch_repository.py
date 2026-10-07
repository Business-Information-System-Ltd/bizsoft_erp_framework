"""Persistence helper for branch master data."""
from django.db.models import Q
from erp_organization.repositories.organization_unit_repository import OrganizationUnitRepository
from erp_organization.models import BranchProfile

class BranchRepository(OrganizationUnitRepository):
    def get_filtered_branches(self, filters=None):
        filters = filters or {}
        qs = BranchProfile.objects.select_related(
            "organization_unit", "legal_entity", "region", "zone",
            "address", "address__region", "address__zone",
        )
        is_active = filters.get("is_active")
        if is_active:
            value = str(is_active).upper()
            if value == "ACTIVE": qs = qs.filter(is_active=True)
            elif value == "INACTIVE": qs = qs.filter(is_active=False)
        for key in ("region", "zone", "legal_entity", "address"):
            value = filters.get(key)
            if value not in (None, ""):
                qs = qs.filter(**{f"{key}_id": value})
        region_code = filters.get("region_code")
        zone_code = filters.get("zone_code")
        if region_code:
            qs = qs.filter(region__region_code__iexact=region_code)
        if zone_code:
            qs = qs.filter(zone__zone_code__iexact=zone_code)
        branch_type = filters.get("branch_type")
        if branch_type:
            qs = qs.filter(branch_type=branch_type)
        search = filters.get("search")
        if search:
            qs = qs.filter(
                Q(branch_code__icontains=search) |
                Q(branch_name__icontains=search) |
                Q(branch_type__icontains=search) |
                Q(region__region_name__icontains=search) |
                Q(region__region_code__icontains=search) |
                Q(zone__zone_name__icontains=search) |
                Q(zone__zone_code__icontains=search) |
                Q(address__address_line_1__icontains=search) |
                Q(address__township__icontains=search) |
                Q(address__city__icontains=search)
            )
        return qs.order_by("branch_code")

    def get_by_id(self, branch_id):
        return self.get_filtered_branches({}).filter(pk=branch_id).first()
