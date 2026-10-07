from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from erp_organization.models import (
    LegalEntityProfile,
    OrganizationUnit,
    Region,
    Zone,
    Address,
    BranchProfile,
    DepartmentProfile,
    PhysicalLocationProfile,
    CostCenterProfile,
)
from erp_organization.constants import OrganizationUnitType, PhysicalLocationType, UnitStatus
from erp_partners.models import Partner, PartnerRole
from erp_partners.enums.partner_enums import PartnerType, PartnerStatus, PartnerRoleType


class Command(BaseCommand):
    help = "Create FAR test reference data for branch, department, location, cost center, supplier and custodians."

    @transaction.atomic
    def handle(self, *args, **options):
        # Do not create another legal entity. FAR currently uses legal_entity_id=1.
        try:
            legal_entity = LegalEntityProfile.objects.select_related(
                "organization_unit"
            ).get(pk=1)
        except LegalEntityProfile.DoesNotExist:
            raise CommandError(
                "LegalEntityProfile id=1 was not found. "
                "Create/verify the existing legal entity first."
            )

        legal_ou = legal_entity.organization_unit

        # ------------------------------------------------------------
        # 1. Region / Zone / Address
        # ------------------------------------------------------------
        region, _ = Region.objects.update_or_create(
            region_code="YGN",
            defaults={
                "region_name": "Yangon",
                "timezone_name": "Asia/Yangon",
                "map_latitude": 16.8409,
                "map_longitude": 96.1735,
                "is_active": True,
            },
        )

        zone, _ = Zone.objects.get_or_create(
            zone_code="YGN-CBD",
            defaults={
                "zone_name": "Yangon CBD",
                "region": region,
                "is_active": True,
            },
        )
        if zone.region_id != region.id or not zone.is_active:
            zone.region = region
            zone.zone_name = "Yangon CBD"
            zone.is_active = True
            zone.save()

        address, _ = Address.objects.update_or_create(
            address_line_1="BizSoft Yangon Head Office",
            township="Bahan",
            city="Yangon",
            defaults={
                "address_line_2": "Floor 2",
                "region": region,
                "zone": zone,
                "postal_code": "11201",
                "is_active": True,
            },
        )

        # ------------------------------------------------------------
        # 2. Branch
        # ------------------------------------------------------------
        branch_ou, _ = OrganizationUnit.objects.get_or_create(
            unit_code="YGN-HO",
            unit_type=OrganizationUnitType.BRANCH,
            defaults={
                "unit_name": "Yangon Head Office",
                "legal_entity": legal_ou,
                "parent_unit": legal_ou,
                "status": UnitStatus.ACTIVE,
                "is_cost_center": True,
                "is_profit_center": True,
                "is_asset_assignable": True,
                "is_active": True,
                "effective_from": date(2026, 1, 1),
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
            },
        )

        branch, _ = BranchProfile.objects.get_or_create(
            branch_code="YGN-HO",
            defaults={
                "organization_unit": branch_ou,
                "branch_name": "Yangon Head Office",
                "legal_entity": legal_entity,
                "branch_type": "HEAD_OFFICE",
                "region": region,
                "zone": zone,
                "address": address,
                "latitude": 16.8409,
                "longitude": 96.1735,
                "is_head_office": True,
                "is_bank_branch": False,
                "is_active": True,
            },
        )

        # Repair an existing partial record if the code already existed.
        if branch.organization_unit_id != branch_ou.id:
            branch.organization_unit = branch_ou
        branch.legal_entity = legal_entity
        branch.region = region
        branch.zone = zone
        branch.address = address
        branch.is_active = True
        branch.save()

        # ------------------------------------------------------------
        # 3. Department
        # ------------------------------------------------------------
        dept_ou, _ = OrganizationUnit.objects.get_or_create(
            unit_code="IT",
            unit_type=OrganizationUnitType.DEPARTMENT,
            defaults={
                "unit_name": "Information Technology",
                "legal_entity": legal_ou,
                "parent_unit": branch_ou,
                "status": UnitStatus.ACTIVE,
                "is_asset_assignable": True,
                "is_active": True,
                "effective_from": date(2026, 1, 1),
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
            },
        )

        department, _ = DepartmentProfile.objects.get_or_create(
            department_code="IT",
            defaults={
                "organization_unit": dept_ou,
                "department_name": "Information Technology",
                "legal_entity": legal_entity,
                "branch": branch,
                "parent_department": None,
                "is_active": True,
            },
        )

        if department.organization_unit_id != dept_ou.id:
            department.organization_unit = dept_ou
        department.legal_entity = legal_entity
        department.branch = branch
        department.is_active = True
        department.save()

        # ------------------------------------------------------------
        # 4. Physical Location
        # ------------------------------------------------------------
        location_ou, _ = OrganizationUnit.objects.get_or_create(
            unit_code="YGN-HO-F2-R201",
            unit_type=OrganizationUnitType.PHYSICAL_LOCATION,
            defaults={
                "unit_name": "Yangon Head Office - Floor 2 Room 201",
                "legal_entity": legal_ou,
                "parent_unit": branch_ou,
                "status": UnitStatus.ACTIVE,
                "is_asset_assignable": True,
                "is_active": True,
                "effective_from": date(2026, 1, 1),
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
            },
        )

        location, _ = PhysicalLocationProfile.objects.get_or_create(
            location_code="YGN-HO-F2-R201",
            defaults={
                "organization_unit": location_ou,
                "location_name": "Yangon Head Office - Floor 2 Room 201",
                "location_type": PhysicalLocationType.BRANCH_OFFICE,
                "legal_entity": legal_ou,
                "responsible_branch": branch,
                "responsible_department": department,
                "address": "BizSoft Yangon Head Office, Floor 2 / Room 201",
                "is_internal": True,
                "is_asset_assignable": True,
                "is_inventory_storable": False,
                "is_active": True,
            },
        )

        if location.organization_unit_id != location_ou.id:
            location.organization_unit = location_ou
        location.legal_entity = legal_ou
        location.responsible_branch = branch
        location.responsible_department = department
        location.is_asset_assignable = True
        location.is_active = True
        location.save()

        # ------------------------------------------------------------
        # 5. Cost Center (also used by FAR financial_info.cost_center_id)
        # ------------------------------------------------------------
        cc_ou, _ = OrganizationUnit.objects.get_or_create(
            unit_code="CC-IT-YGN",
            unit_type=OrganizationUnitType.COST_CENTER,
            defaults={
                "unit_name": "IT - Yangon",
                "legal_entity": legal_ou,
                "parent_unit": dept_ou,
                "status": UnitStatus.ACTIVE,
                "is_cost_center": True,
                "is_active": True,
                "effective_from": date(2026, 1, 1),
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
            },
        )

        cost_center, _ = CostCenterProfile.objects.get_or_create(
            cost_center_code="CC-IT-YGN",
            defaults={
                "organization_unit": cc_ou,
                "cost_center_name": "IT - Yangon",
                "legal_entity": legal_ou,
                "branch": branch_ou,
                "department": dept_ou,
                "is_active": True,
            },
        )

        if cost_center.organization_unit_id != cc_ou.id:
            cost_center.organization_unit = cc_ou
        cost_center.legal_entity = legal_ou
        cost_center.branch = branch_ou
        cost_center.department = dept_ou
        cost_center.is_active = True
        cost_center.save()

        # ------------------------------------------------------------
        # 6. Supplier Partner + SUPPLIER role
        # ------------------------------------------------------------
        supplier, _ = Partner.objects.get_or_create(
            partner_code="SUP-ABC-001",
            defaults={
                "partner_type": PartnerType.LEGAL_PERSON,
                "display_name": "ABC Technology Co., Ltd.",
                "legal_name": "ABC Technology Co., Ltd.",
                "short_name": "ABC Technology",
                "status": PartnerStatus.ACTIVE,
                "country_code": "MM",
                "default_language": "en",
                "default_currency_code": "MMK",
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
                "is_active": True,
            },
        )

        supplier.status = PartnerStatus.ACTIVE
        supplier.is_active = True
        supplier.save(update_fields=["status", "is_active", "updated_at"])

        PartnerRole.objects.update_or_create(
            partner=supplier,
            role_type=PartnerRoleType.SUPPLIER,
            defaults={
                "effective_from": date(2026, 1, 1),
                "effective_to": None,
                "status": PartnerStatus.ACTIVE,
                "is_primary_role": True,
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
                "is_active": True,
            },
        )

        # ------------------------------------------------------------
        # 7. Custodian Partner + ASSET_CUSTODIAN role
        # ------------------------------------------------------------
        custodian, _ = Partner.objects.get_or_create(
            partner_code="EMP-IT-001",
            defaults={
                "partner_type": PartnerType.NATURAL_PERSON,
                "display_name": "Aung Aung - IT",
                "legal_name": "Aung Aung",
                "short_name": "Aung Aung",
                "status": PartnerStatus.ACTIVE,
                "country_code": "MM",
                "default_language": "my",
                "default_currency_code": "MMK",
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
                "is_active": True,
            },
        )

        custodian.status = PartnerStatus.ACTIVE
        custodian.is_active = True
        custodian.save(update_fields=["status", "is_active", "updated_at"])

        PartnerRole.objects.update_or_create(
            partner=custodian,
            role_type=PartnerRoleType.ASSET_CUSTODIAN,
            defaults={
                "effective_from": date(2026, 1, 1),
                "effective_to": None,
                "status": PartnerStatus.ACTIVE,
                "is_primary_role": True,
                "created_by": "seed_far_reference_data",
                "updated_by": "seed_far_reference_data",
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("FAR reference data is ready."))
        self.stdout.write("")
        self.stdout.write(f"legal_entity_id      = {legal_entity.id}")
        self.stdout.write(f"branch_id            = {branch.id}")
        self.stdout.write(f"department_id        = {department.id}")
        self.stdout.write(f"location_id          = {location.id}")
        self.stdout.write(f"cost_center_id       = {cost_center.id}")
        self.stdout.write(f"supplier_partner_id  = {supplier.id}")
        self.stdout.write(f"custodian_partner_id = {custodian.id}")
        self.stdout.write("")
        self.stdout.write("Use these IDs in the FAR AssetCreate payload.")
