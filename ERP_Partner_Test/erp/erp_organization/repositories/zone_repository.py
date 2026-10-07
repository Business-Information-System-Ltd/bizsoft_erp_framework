"""Persistence helper for zone master."""
from django.db.models import Q
from erp_organization.models import Zone
class ZoneRepository:
    def get_filtered_zones(self, filters=None):
        filters=filters or {}; qs=Zone.objects.select_related("region")
        value=filters.get("is_active")
        if value not in (None, ""):
            value=str(value).upper()
            if value in ("TRUE","1","ACTIVE"): qs=qs.filter(is_active=True)
            elif value in ("FALSE","0","INACTIVE"): qs=qs.filter(is_active=False)
        region=filters.get("region",filters.get("region_id"))
        if region: qs=qs.filter(region_id=region)
        if filters.get("zone_code"): qs=qs.filter(zone_code__iexact=filters["zone_code"])
        if filters.get("search"):
            q=filters["search"]; qs=qs.filter(Q(zone_code__icontains=q)|Q(zone_name__icontains=q)|Q(region__region_name__icontains=q))
        return qs.order_by("zone_name")
    def get_by_id(self, zone_id): return Zone.objects.select_related("region").filter(pk=zone_id).first()
