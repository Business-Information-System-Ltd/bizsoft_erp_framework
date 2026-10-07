"""
BizSoft ERP - Partners Module

File:
    erp_partners/urls.py

Purpose:
    Defines partner API routes.

Architectural Notes:
    - This module manages common Business Partner / Stakeholder master data.
    - Customer, Supplier, Employee, FAR, Finance, and other module-specific profiles
      must be implemented in their respective modules.
    - This module should remain a core shared service with minimum external dependency.

Author:
    BizSoft Systems

Created:
    2026-06-04
"""


from django.urls import include, path
from rest_framework.routers import DefaultRouter
from erp_partners.views.partner_compliance_views import PartnerComplianceSummaryAPIView
from erp_partners.views.check_duplicate_view import (
    CheckDuplicateAPIView
)
from erp_partners.views.legal_entity_views import LegalEntityProfileViewSet
from erp_partners.views import PartnerRelationshipViewSet, PartnerUsageValidationView, PartnerViewSet
from erp_partners.views.validate_role_change_view import (
    ValidateRoleChangeAPIView
)
from erp_partners.views.create_with_context_view import (
    CreatePartnerWithContextAPIView
)
from erp_partners.views.system_constants_view import (
    SystemConstantsAPIView
)
router = DefaultRouter()
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'partner-relationships', PartnerRelationshipViewSet, basename='partner-relationship')
router.register(
    r'partner-legal-entities',
    LegalEntityProfileViewSet,
    basename='legal-entity'
)


urlpatterns = [
    path('partners/validate-usage/', PartnerUsageValidationView.as_view(), name='partner-validate-usage'),
    path(
        "partners/check-duplicate/",
        CheckDuplicateAPIView.as_view(),
        name="check-duplicate"
    ),
      path(
        "partners/validate-role-change/",
        ValidateRoleChangeAPIView.as_view(),
        name="validate-role-change"
    ),
    path(
        "partners/create-with-context/",
        CreatePartnerWithContextAPIView.as_view(),
        name="create-with-context"
    ),
    path(
        "system/constants/",
        SystemConstantsAPIView.as_view(),
        name="system-constants"
    ),
    path(
        "partners/<uuid:partner_id>/compliance_summary/",
        PartnerComplianceSummaryAPIView.as_view(),
        name="partner-compliance"
    ),
    # path(
    #     "{id}/summzary/",
    #     SystemConstantsAPIView.as_view(),
    #     name="system-constants"
    # ),
    path('', include(router.urls)),
]

