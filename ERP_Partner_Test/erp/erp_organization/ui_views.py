"""
BizSoft ERP - ERP Organization

Company: Business Information Systems Ltd. / BizSoft
Author: Business Information Systems Ltd. / BizSoft
Package: erp_organization
Version: 1.0.0

Purpose:
This file is part of the erp_organization ERP business foundation package.

Important:
- This package defines legal entities, branches, departments, SBUs, facilities,
  warehouses, projects, cost centers, profit centers, physical locations,
  custodians, and flexible organization relationships.
- Organization tells where and who.
- Dimension tells how to classify, summarize, analyze, and report.
- Do not implement accounting posting, inventory movement, FAR depreciation,
  payroll, workflow routing, permission engine, audit trail, or notifications.
- core_* packages must not depend on erp_organization.

Rule:
Selectors read data.
Domain Policies validate domain truth.
Application Policies validate whether an action is allowed in context.
Application Services orchestrate use cases.

File Purpose:
Defines server-rendered sample UI views for ERP organization.
"""


from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from erp_organization.constants import OrganizationUnitType, PhysicalLocationType
from erp_organization.forms import BranchForm, DepartmentForm, LegalEntityForm, PhysicalLocationForm
from erp_organization.models import BranchProfile, DepartmentProfile, LegalEntityProfile, OrganizationUnit, PhysicalLocationProfile
from erp_organization.services.branch_application_service import BranchApplicationService
from erp_organization.services.department_application_service import DepartmentApplicationService
from erp_organization.services.hierarchy_service import OrganizationHierarchyService
from erp_organization.services.legal_entity_application_service import LegalEntityApplicationService
from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService


def _handle_form(request, form_class, service_method, success_message):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            service_method(user=request.user if request.user.is_authenticated else None, data=form.cleaned_data)
            messages.success(request, success_message)
            return redirect("erp-org-ui-dashboard")
        except (IntegrityError, Exception) as exc:
            messages.error(request, str(exc))
    return form, None


def dashboard(request):
    context = {
        "counts": {
            "legal_entities": LegalEntityProfile.objects.filter(is_active=True).count(),
            "branches": BranchProfile.objects.filter(is_active=True).count(),
            "departments": DepartmentProfile.objects.filter(is_active=True).count(),
            "locations": PhysicalLocationProfile.objects.filter(is_active=True).count(),
            "inactive_units": OrganizationUnit.objects.filter(is_active=False).count(),
        },
        "recent_units": OrganizationUnit.objects.order_by("-created_at")[:10],
        "tree": OrganizationHierarchyService.get_tree(),
    }
    return render(request, "erp_organization/dashboard.html", context)


def units(request):
    unit_type = request.GET.get("unit_type") or ""
    query = OrganizationUnit.objects.all().order_by("unit_type", "unit_code")
    if unit_type:
        query = query.filter(unit_type=unit_type)
    return render(request, "erp_organization/units.html", {"units": query, "unit_type": unit_type, "unit_types": OrganizationUnitType.CHOICES})


def legal_entities(request):
    form, response = _handle_form(request, LegalEntityForm, LegalEntityApplicationService.create_legal_entity, "Legal entity created.")
    if response:
        return response
    return render(request, "erp_organization/legal_entities.html", {"form": form, "items": LegalEntityProfile.objects.order_by("legal_entity_code")})


def branches(request):
    form, response = _handle_form(request, BranchForm, BranchApplicationService.create_branch, "Branch created.")
    if response:
        return response
    return render(request, "erp_organization/branches.html", {"form": form, "items": BranchProfile.objects.order_by("branch_code")})


def departments(request):
    form, response = _handle_form(request, DepartmentForm, DepartmentApplicationService.create_department, "Department created.")
    if response:
        return response
    return render(request, "erp_organization/departments.html", {"form": form, "items": DepartmentProfile.objects.order_by("department_code")})


def locations(request):
    form, response = _handle_form(request, PhysicalLocationForm, PhysicalLocationApplicationService.create_physical_location, "Physical location created.")
    if response:
        return response
    return render(request, "erp_organization/locations.html", {"form": form, "items": PhysicalLocationProfile.objects.order_by("location_code")})


@require_POST
def seed_sample_bank(request):
    try:
        if not LegalEntityProfile.objects.filter(legal_entity_code="ABC_BANK").exists():
            LegalEntityApplicationService.create_legal_entity(data={
                "legal_entity_code": "ABC_BANK",
                "legal_entity_name": "ABC Bank Limited",
                "country_code": "MMR",
                "functional_currency_code": "MMK",
            })
        if not BranchProfile.objects.filter(branch_code="HO").exists():
            BranchApplicationService.create_branch(data={
                "branch_code": "HO",
                "branch_name": "Head Office",
                "legal_entity_code": "ABC_BANK",
                "is_head_office": True,
                "is_bank_branch": True,
            })
        if not BranchProfile.objects.filter(branch_code="YGN").exists():
            BranchApplicationService.create_branch(data={
                "branch_code": "YGN",
                "branch_name": "Yangon Main Branch",
                "legal_entity_code": "ABC_BANK",
                "region_code": "YGN_REGION",
                "zone_code": "LOWER_MYANMAR",
                "is_bank_branch": True,
            })
        for code, name in [("FIN", "Finance"), ("IT", "Information Technology"), ("OPS", "Operations")]:
            if not DepartmentProfile.objects.filter(department_code=code).exists():
                DepartmentApplicationService.create_department(data={
                    "department_code": code,
                    "department_name": name,
                    "legal_entity_code": "ABC_BANK",
                    "branch_code": "HO",
                })
        if not PhysicalLocationProfile.objects.filter(location_code="ATM_JC").exists():
            PhysicalLocationApplicationService.create_physical_location(data={
                "location_code": "ATM_JC",
                "location_name": "ATM Junction City",
                "location_type": PhysicalLocationType.ATM_SITE,
                "responsible_branch_code": "YGN",
                "is_internal": False,
                "is_asset_assignable": True,
            })
        messages.success(request, "Sample bank organization data is ready.")
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect("erp-org-ui-dashboard")
