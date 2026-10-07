from erp_partners.models import Partner


def _search_partner_by_role(
    *,
    role_type,
    search=None,
):
    qs = (
        Partner.objects
        .filter(
            is_active=True,
            roles__role_type=role_type,
            roles__status="ACTIVE",
        )
        .distinct()
        .order_by(
            "display_name",
            "partner_code",
        )
    )

    if search:
        qs = qs.filter(
            display_name__icontains=search
        ) | qs.filter(
            partner_code__icontains=search
        )

    return qs


def search_suppliers(search=None):
    return _search_partner_by_role(
        role_type="SUPPLIER",
        search=search,
    )


def search_custodians(search=None):
    return _search_partner_by_role(
        role_type="ASSET_CUSTODIAN",
        search=search,
    )


def search_employees(search=None):
    return _search_partner_by_role(
        role_type="EMPLOYEE",
        search=search,
    )