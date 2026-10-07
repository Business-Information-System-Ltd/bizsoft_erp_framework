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
Defines organization API routes.
"""


from django.urls import path
from erp_organization import ui_views, views
# from .views import delete_region
from erp_organization.views import BranchPDFExportView, LegalEntityPDFExportView, DepartmentPDFExportView,PhysicalLocationPDFExportView
from erp_organization.views import LocationTypeConfigAPIView
urlpatterns=[]
if views.OrganizationUnitListView:
    urlpatterns += [
        path('units/',views.OrganizationUnitListView.as_view(),name='erp-org-units'),
        path('legal-entities/',views.LegalEntityListCreateView.as_view(),name='erp-org-legal-entities'),
        path('regions/',views.RegionListView.as_view(),name='erp-org-regions'),
        path(
            'regions/<int:region_id>/',
            views.RegionDetailView.as_view(),
            name='erp-org-region-detail',
        ),
        path('zones/',views.ZoneListView.as_view(),name='erp-org-zones'),
        path(
            'zones/<int:zone_id>/',
            views.ZoneDetailView.as_view(),
            name='erp-org-zone-detail',
        ),
        path('addresses/',views.AddressListView.as_view(),name='erp-org-addresses'),
        path(
            'addresses/<int:address_id>/',
            views.AddressDetailView.as_view(),
            name='erp-org-address-detail',
        ),
        path('branches/',views.BranchListCreateView.as_view(),name='erp-org-branches'),
        path('branches/<int:branch_id>/',views.BranchDetailView.as_view(), name='erp-org-branch-detail',),
        path('departments/',views.DepartmentListCreateView.as_view(),name='erp-org-departments'),
        path('cost-centers/',views.CostCenterListView.as_view(),name='erp-org-cost-centers'),
        path('profit-centers/',views.ProfitCenterListView.as_view(),name='erp-org-profit-centers'),
        path('physical-locations/',views.PhysicalLocationListCreateView.as_view(),name='erp-org-physical-locations'),
        # path('locations/',views.PhysicalLocationListView.as_view(),name='erp-org-locations'),
        path('tree/',views.OrganizationTreeView.as_view(),name='erp-org-tree'),
        path('bank/branches/',views.BankBranchListView.as_view(),name='erp-org-bank-branches'),
        path('bank/atm-locations/',views.ATMLocationListView.as_view(),name='erp-org-atm-locations'),
        path(
        "location-types/<str:location_type>/fields/",LocationTypeConfigAPIView.as_view(),),
        # path("organization/regions/<int:pk>/delete/",delete_region,name="delete-region",),
        
        
        
   
        path("organization/legal-entities/export/pdf/", LegalEntityPDFExportView.as_view(), name="erp-org-legal-entities-export-pdf"),
        path("organization/branches/export/pdf/", BranchPDFExportView.as_view(), name="erp-org-branches-export-pdf"),
        path("organization/departments/export/pdf/", DepartmentPDFExportView.as_view(), name="erp-org-departments-export-pdf"),
        path("organization/physical-locations/export/pdf/", PhysicalLocationPDFExportView.as_view(), name="erp-org-physical-locations-export-pdf"),
    ]

urlpatterns += [
    path('ui/', ui_views.dashboard, name='erp-org-ui-dashboard'),
    path('ui/units/', ui_views.units, name='erp-org-ui-units'),
    path('ui/legal-entities/', ui_views.legal_entities, name='erp-org-ui-legal-entities'),
    path('ui/branches/', ui_views.branches, name='erp-org-ui-branches'),
    path('ui/departments/', ui_views.departments, name='erp-org-ui-departments'),
    path('ui/locations/', ui_views.locations, name='erp-org-ui-locations'),
    path('ui/seed-bank/', ui_views.seed_sample_bank, name='erp-org-ui-seed-bank'),
]
