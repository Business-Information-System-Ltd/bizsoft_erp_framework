"""Persistence helper for address master."""
from django.db.models import Q
from erp_organization.models import Address
class AddressRepository:
    def get_filtered_addresses(self, filters=None):
        filters=filters or {}; qs=Address.objects.select_related("region","zone")
        value=filters.get("is_active")
        if value not in (None, ""):
            value=str(value).upper()
            if value in ("TRUE","1","ACTIVE"): qs=qs.filter(is_active=True)
            elif value in ("FALSE","0","INACTIVE"): qs=qs.filter(is_active=False)
        region=filters.get("region",filters.get("region_id")); zone=filters.get("zone",filters.get("zone_id"))
        if region: qs=qs.filter(region_id=region)
        if zone: qs=qs.filter(zone_id=zone)
        if filters.get("city"): qs=qs.filter(city__icontains=filters["city"])
        if filters.get("township"): qs=qs.filter(township__icontains=filters["township"])
        if filters.get("search"):
            q=filters["search"]; qs=qs.filter(Q(address_line_1__icontains=q)|Q(address_line_2__icontains=q)|Q(township__icontains=q)|Q(city__icontains=q)|Q(postal_code__icontains=q)|Q(region__region_name__icontains=q)|Q(zone__zone_name__icontains=q))
        return qs.order_by("city","township","address_line_1")
    def get_by_id(self, address_id): return Address.objects.select_related("region","zone").filter(pk=address_id).first()
