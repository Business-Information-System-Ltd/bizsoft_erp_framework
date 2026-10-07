from django.urls import path

from core_entity_django.views import (
    AssetListCreateView,
    AssetDetailView,
    AssetValidateView,
    BulkValidateView,
    AssetCapitalizeView,
    BulkCapitalizeView,
    BulkDeleteView,
    AssetApprovalPdfView,
    BulkApprovalPdfView,
    AssetApprovalActionView,
    AssetDocumentListCreateView,
    AssetImportView,
    WipTransferView,
    AssetExportView,
)


urlpatterns = [

    path(
        "assets-core/",
        AssetListCreateView.as_view(),
        name="far-asset-list-create",
    ),

    path(
        "assets-core/export/",
        AssetExportView.as_view(),
        name="far-asset-export",
    ),

    path(
        "assets-core/import/",
        AssetImportView.as_view(),
        name="far-asset-import",
    ),

    path(
        "assets-core/wip-transfer/",
        WipTransferView.as_view(),
        name="far-wip-transfer",
    ),

    path(
        "assets-core/bulk-validate/",
        BulkValidateView.as_view(),
        name="far-bulk-validate",
    ),

    path(
        "assets-core/bulk-delete/",
        BulkDeleteView.as_view(),
        name="far-bulk-delete",
    ),

    path(
        "assets-core/bulk-capitalize/",
        BulkCapitalizeView.as_view(),
        name="far-bulk-capitalize",
    ),

    path(
        "assets-core/bulk-print/",
        BulkApprovalPdfView.as_view(),
        name="far-bulk-print",
    ),

    path(
        "assets-core/<int:pk>/",
        AssetDetailView.as_view(),
        name="far-asset-detail",
    ),

    path(
        "assets-core/<int:pk>/validate/",
        AssetValidateView.as_view(),
        name="far-asset-validate",
    ),

    path(
        "assets-core/<int:pk>/capitalize/",
        AssetCapitalizeView.as_view(),
        name="far-asset-capitalize",
    ),

    path(
        "assets-core/<int:pk>/approval-pdf/",
        AssetApprovalPdfView.as_view(),
        name="far-asset-approval-pdf",
    ),

    path(
        "assets-core/<int:pk>/approval/",
        AssetApprovalActionView.as_view(),
        name="far-asset-approval",
    ),

    path(
        "assets-core/<int:pk>/documents/",
        AssetDocumentListCreateView.as_view(),
        name="far-asset-documents",
    ),
]