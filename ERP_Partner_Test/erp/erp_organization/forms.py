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
Defines simple Django forms for the sample organization UI.
"""


from django import forms

from erp_organization.constants import PhysicalLocationType


class LegalEntityForm(forms.Form):
    legal_entity_code = forms.CharField(max_length=50)
    legal_entity_name = forms.CharField(max_length=255)
    country_code = forms.CharField(max_length=10, initial="MMR")
    functional_currency_code = forms.CharField(max_length=10, initial="MMK")
    presentation_currency_code = forms.CharField(max_length=10, required=False)


class BranchForm(forms.Form):
    branch_code = forms.CharField(max_length=50)
    branch_name = forms.CharField(max_length=255)
    legal_entity_code = forms.CharField(max_length=50)
    region_code = forms.CharField(max_length=50, required=False)
    zone_code = forms.CharField(max_length=50, required=False)
    is_head_office = forms.BooleanField(required=False)
    is_bank_branch = forms.BooleanField(required=False, initial=True)


class DepartmentForm(forms.Form):
    department_code = forms.CharField(max_length=50)
    department_name = forms.CharField(max_length=255)
    legal_entity_code = forms.CharField(max_length=50)
    branch_code = forms.CharField(max_length=50, required=False)
    parent_department_code = forms.CharField(max_length=50, required=False)


class PhysicalLocationForm(forms.Form):
    location_code = forms.CharField(max_length=50)
    location_name = forms.CharField(max_length=255)
    location_type = forms.ChoiceField(choices=PhysicalLocationType.CHOICES, initial=PhysicalLocationType.BRANCH_OFFICE)
    responsible_branch_code = forms.CharField(max_length=50, required=False)
    responsible_department_code = forms.CharField(max_length=50, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
    is_internal = forms.BooleanField(required=False, initial=True)
    is_asset_assignable = forms.BooleanField(required=False)
    is_inventory_storable = forms.BooleanField(required=False)
