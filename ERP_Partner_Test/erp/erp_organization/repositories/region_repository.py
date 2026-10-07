"""Persistence helper for region master."""
from django.db.models import Q
from erp_organization.models import Region
class RegionRepository:
    def get_filtered_regions(self, filters=None):
        filters=filters or {}; qs=Region.objects.all()
        value=filters.get("is_active")
        if value not in (None, ""):
            value=str(value).upper()
            if value in ("TRUE","1","ACTIVE"): qs=qs.filter(is_active=True)
            elif value in ("FALSE","0","INACTIVE"): qs=qs.filter(is_active=False)
        if filters.get("region_code"): qs=qs.filter(region_code__iexact=filters["region_code"])
        if filters.get("search"):
            q=filters["search"]; qs=qs.filter(Q(region_code__icontains=q)|Q(region_name__icontains=q))
        return qs.order_by("region_name")
    def get_by_id(self, region_id): return Region.objects.filter(pk=region_id).first()
