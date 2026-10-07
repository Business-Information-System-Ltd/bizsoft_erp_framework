# from django.core.exceptions import ValidationError

# from rest_framework import status
# from rest_framework.parsers import (
#     JSONParser,
#     MultiPartParser,
#     FormParser,
# )
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from django.conf import settings
# from rest_framework.permissions import AllowAny
# from core_entity_django.application_policies.asset_core_policy import (
#     require_permission,
# )

# from core_entity_django.models import AssetCore

# from core_entity_django.selectors.asset_core_selectors import (
#     get_asset,
#     list_draft_assets,
#     get_capitalization_candidates,
# )

# from core_entity_django.serializers.asset_core_serializers import (
#     AssetCoreSerializer,
#     AssetCreateSerializer,
#     AssetUpdateSerializer,
#     DeleteAssetSerializer,
#     BulkAssetSerializer,
#     BulkDeleteSerializer,
#     BulkCapitalizeSerializer,
#     ApprovalActionSerializer,
#     AssetDocumentSerializer,
#     ImportAssetSerializer,
#     WipTransferSerializer,
# )

# from core_entity_django.services.asset_core_services import (
#     create_asset,
#     update_asset,
#     validate_asset,
#     delete_asset,
#     capitalize_asset,
# )

# from core_entity_django.services.asset_bulk_service import (
#     bulk_validate,
#     bulk_delete,
# )

# from core_entity_django.services.asset_approval_service import (
#     generate_approval_pdf,
#     generate_bulk_approval_pdf,
# )

# from core_entity_django.services.asset_approval_action_service import (
#     approval_action,
# )

# from core_entity_django.services.asset_import_service import (
#     import_assets,
# )

# from core_entity_django.services.wip_transfer_service import (
#     transfer_wip_to_assets,
# )

# from core_entity_django.services.asset_export_service import (
#     export_xlsx,
#     export_pdf,
# )


# def _request_context(request):
#     forwarded = request.META.get(
#         "HTTP_X_FORWARDED_FOR"
#     )

#     source_ip = (
#         forwarded.split(",")[0].strip()
#         if forwarded
#         else request.META.get("REMOTE_ADDR")
#     )

#     device = request.META.get(
#         "HTTP_USER_AGENT",
#         "",
#     )

#     return source_ip, device


# class AssetListCreateView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )
    
    
#     def get(self, request):

#         require_permission(
#             request.user,
#             "view",
#         )

#         filters = {
#             "draft_date_from": request.query_params.get(
#                 "draft_date_from"
#             ),
#             "draft_date_to": request.query_params.get(
#                 "draft_date_to"
#             ),
#             "acquisition_date_from": request.query_params.get(
#                 "acquisition_date_from"
#             ),
#             "acquisition_date_to": request.query_params.get(
#                 "acquisition_date_to"
#             ),
#             "asset_class": request.query_params.get(
#                 "asset_class"
#             ),
#             "asset_category": request.query_params.get(
#                 "asset_category"
#             ),
#             "asset_type": request.query_params.get(
#                 "asset_type"
#             ),
#             "source": request.query_params.get(
#                 "source"
#             ),
#             "company": request.query_params.get(
#                 "company"
#             ),
#             "branch": request.query_params.get(
#                 "branch"
#             ),
#             "department": request.query_params.get(
#                 "department"
#             ),
#             "supplier": request.query_params.get(
#                 "supplier"
#             ),
#             "validation_status": request.query_params.get(
#                 "validation_status"
#             ),
#             "capitalization_eligible": (
#                 request.query_params.get(
#                     "capitalization_eligible"
#                 )
#             ),
#             "prepared_by": request.query_params.get(
#                 "prepared_by"
#             ),
#             "import_batch": request.query_params.get(
#                 "import_batch"
#             ),
#             "wip_reference": request.query_params.get(
#                 "wip_reference"
#             ),
#             "keyword": request.query_params.get(
#                 "keyword"
#             ),
#         }

#         if (
#             filters["capitalization_eligible"]
#             in (None, "")
#         ):
#             filters["capitalization_eligible"] = None
#         else:
#             filters["capitalization_eligible"] = (
#                 filters["capitalization_eligible"].lower()
#                 == "true"
#             )

#         filters = {
#             key: value
#             for key, value in filters.items()
#             if value not in (
#                 None,
#                 "",
#             )
#         }

#         queryset = list_draft_assets(
#             filters
#         )

#         return Response(
#             AssetCoreSerializer(
#                 queryset,
#                 many=True,
#             ).data
#         )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "create",
#         )

#         serializer = AssetCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         asset = create_asset(
#             user=request.user,
#             validated_data=serializer.validated_data,
#             source_ip=source_ip,
#             device=device,
#         )

#         return Response(
#             AssetCoreSerializer(asset).data,
#             status=status.HTTP_201_CREATED,
#         )


# class AssetDetailView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def get(self, request, pk):

#         require_permission(
#             request.user,
#             "view",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         return Response(
#             AssetCoreSerializer(asset).data
#         )

#     def put(self, request, pk):
#         return self._update(request, pk)

#     def patch(self, request, pk):
#         return self._update(request, pk)

#     def _update(self, request, pk):

#         require_permission(
#             request.user,
#             "edit",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = AssetUpdateSerializer(
#             data=request.data,
#             partial=True,
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             asset = update_asset(
#                 asset=asset,
#                 user=request.user,
#                 validated_data=serializer.validated_data,
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response(
#             AssetCoreSerializer(asset).data
#         )

#     def delete(self, request, pk):

#         require_permission(
#             request.user,
#             "delete",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = DeleteAssetSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             delete_asset(
#                 asset=asset,
#                 user=request.user,
#                 reason=serializer.validated_data["reason"],
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response({
#             "detail": (
#                 "Draft asset deleted successfully."
#             )
#         })


# class AssetValidateView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]
#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request, pk):

#         require_permission(
#             request.user,
#             "validate",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             result = validate_asset(
#                 asset=asset,
#                 user=request.user,
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response({
#             "asset": AssetCoreSerializer(
#                 result["asset"]
#             ).data,
#             "errors": result["errors"],
#             "warnings": result["warnings"],
#         })


# class BulkValidateView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]
#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "bulk_validate",
#         )

#         serializer = BulkAssetSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         assets = list_draft_assets().filter(
#             id__in=serializer.validated_data[
#                 "asset_ids"
#             ]
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         results = bulk_validate(
#             assets=assets,
#             user=request.user,
#             source_ip=source_ip,
#             device=device,
#         )

#         return Response({
#             "results": results
#         })


# class AssetCapitalizeView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]
#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request, pk):

#         require_permission(
#             request.user,
#             "capitalize",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             capitalization = capitalize_asset(
#                 asset=asset,
#                 user=request.user,
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response({
#             "detail": (
#                 "Asset has been capitalized successfully."
#             ),
#             "transaction_reference": (
#                 capitalization.transaction_reference
#             ),
#             "asset_id": capitalization.asset_id,
#         })


# class BulkCapitalizeView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#             [AllowAny]
#             if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#             else [IsAuthenticated]
#         )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "bulk_capitalize",
#         )

#         serializer = BulkCapitalizeSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         assets = get_capitalization_candidates(
#             serializer.validated_data["asset_ids"]
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         results = []

#         for asset in assets:

#             try:

#                 capitalization = capitalize_asset(
#                     asset=asset,
#                     user=request.user,
#                     source_ip=source_ip,
#                     device=device,
#                 )

#                 results.append({
#                     "asset_id": asset.id,
#                     "status": "CAPITALIZED",
#                     "transaction_reference": (
#                         capitalization.transaction_reference
#                     ),
#                 })

#             except ValidationError as exc:

#                 results.append({
#                     "asset_id": asset.id,
#                     "status": "ERROR",
#                     "errors": exc.messages,
#                 })

#         return Response({
#             "results": results
#         })


# class BulkDeleteView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "bulk_delete",
#         )

#         serializer = BulkDeleteSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         assets = list_draft_assets().filter(
#             id__in=serializer.validated_data[
#                 "asset_ids"
#             ]
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         results = bulk_delete(
#             assets=assets,
#             user=request.user,
#             reason=serializer.validated_data["reason"],
#             source_ip=source_ip,
#             device=device,
#         )

#         return Response({
#             "results": results
#         })


# class AssetApprovalPdfView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def get(self, request, pk):

#         require_permission(
#             request.user,
#             "print",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         source_ip, device = _request_context(
#             request
#         )

#         return generate_approval_pdf(
#             asset=asset,
#             user=request.user,
#             source_ip=source_ip,
#             device=device,
#         )


# class BulkApprovalPdfView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "print",
#         )

#         serializer = BulkAssetSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         assets = list_draft_assets().filter(
#             id__in=serializer.validated_data[
#                 "asset_ids"
#             ]
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         return generate_bulk_approval_pdf(
#             assets=assets,
#             user=request.user,
#             source_ip=source_ip,
#             device=device,
#         )


# class AssetApprovalActionView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request, pk):

#         require_permission(
#             request.user,
#             "approve",
#         )

#         serializer = ApprovalActionSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             asset = approval_action(
#                 asset=asset,
#                 user=request.user,
#                 action=serializer.validated_data["action"],
#                 reason=serializer.validated_data.get(
#                     "reason",
#                     "",
#                 ),
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response(
#             AssetCoreSerializer(asset).data
#         )


# class AssetDocumentListCreateView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     parser_classes = [
#         MultiPartParser,
#         FormParser,
#     ]

#     def get(self, request, pk):

#         require_permission(
#             request.user,
#             "view",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         return Response(
#             AssetDocumentSerializer(
#                 asset.documents.all(),
#                 many=True,
#             ).data
#         )

#     def post(self, request, pk):

#         require_permission(
#             request.user,
#             "edit",
#         )

#         asset = get_asset(pk)

#         if not asset:
#             return Response(
#                 {"detail": "Asset not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         serializer = AssetDocumentSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         document = serializer.save(
#             asset=asset,
#             uploaded_by=request.user,
#         )

#         return Response(
#             AssetDocumentSerializer(document).data,
#             status=status.HTTP_201_CREATED,
#         )


# class AssetImportView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     parser_classes = [
#         MultiPartParser,
#         FormParser,
#     ]

#     def post(self, request):

#         require_permission(
#             request.user,
#             "import",
#         )

#         serializer = ImportAssetSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         result = import_assets(
#             user=request.user,
#             uploaded_file=serializer.validated_data[
#                 "file"
#             ],
#             template_version=serializer.validated_data[
#                 "template_version"
#             ],
#             source_ip=source_ip,
#             device=device,
#         )

#         return Response({
#             "batch_number": (
#                 result["batch"].batch_number
#             ),
#             "status": result["batch"].status,
#             "total_rows": result["batch"].total_rows,
#             "valid_rows": result["batch"].valid_rows,
#             "error_rows": result["batch"].error_rows,
#             "errors": result["errors"],
#         })


# class WipTransferView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def post(self, request):

#         require_permission(
#             request.user,
#             "wip_transfer",
#         )

#         serializer = WipTransferSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         source_ip, device = _request_context(
#             request
#         )

#         try:
#             result = transfer_wip_to_assets(
#                 user=request.user,
#                 validated_data=serializer.validated_data,
#                 source_ip=source_ip,
#                 device=device,
#             )

#         except ValidationError as exc:
#             return Response(
#                 {"detail": exc.messages},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response({
#             "created_asset_ids": [
#                 asset.id
#                 for asset in result["assets"]
#             ],
#             "total_allocated": str(
#                 result["total_allocated"]
#             ),
#             "remaining_balance": str(
#                 result["remaining_balance"]
#             ),
#         }, status=status.HTTP_201_CREATED)


# class AssetExportView(APIView):

#     # permission_classes = [
#     #     IsAuthenticated
#     # ]

#     permission_classes = (
#         [AllowAny]
#         if getattr(settings, "FAR_DISABLE_AUTH_FOR_TESTING", False)
#         else [IsAuthenticated]
#     )

#     def get(self, request):

#         require_permission(
#             request.user,
#             "export",
#         )

#         filters = {
#             key: request.query_params.get(key)
#             for key in [
#                 "draft_date_from",
#                 "draft_date_to",
#                 "acquisition_date_from",
#                 "acquisition_date_to",
#                 "asset_class",
#                 "asset_category",
#                 "asset_type",
#                 "source",
#                 "company",
#                 "branch",
#                 "department",
#                 "supplier",
#                 "validation_status",
#                 "keyword",
#             ]
#         }

#         filters = {
#             key: value
#             for key, value in filters.items()
#             if value not in (None, "")
#         }

#         queryset = list_draft_assets(
#             filters
#         )

#         export_format = request.query_params.get(
#             "format",
#             "xlsx",
#         ).lower()

#         if export_format == "pdf":
#             return export_pdf(queryset)

#         return export_xlsx(queryset)


from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    MultiPartParser,
    FormParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from rest_framework.permissions import AllowAny

from core_entity_django.application_policies.asset_core_policy import (
    require_permission,
)

from core_entity_django.models import AssetCore

from core_entity_django.selectors.asset_core_selectors import (
    get_asset,
    list_draft_assets,
    get_capitalization_candidates,
)

from core_entity_django.serializers.asset_core_serializers import (
    AssetCoreSerializer,
    AssetCreateSerializer,
    AssetUpdateSerializer,
    DeleteAssetSerializer,
    BulkAssetSerializer,
    BulkDeleteSerializer,
    BulkCapitalizeSerializer,
    ApprovalActionSerializer,
    AssetDocumentSerializer,
    ImportAssetSerializer,
    WipTransferSerializer,
)

from core_entity_django.services.asset_core_services import (
    create_asset,
    update_asset,
    validate_asset,
    delete_asset,
    capitalize_asset,
)

from core_entity_django.services.asset_bulk_service import (
    bulk_validate,
    bulk_delete,
)

from core_entity_django.services.asset_approval_service import (
    generate_approval_pdf,
    generate_bulk_approval_pdf,
)

from core_entity_django.services.asset_approval_action_service import (
    approval_action,
)

from core_entity_django.services.asset_import_service import (
    import_assets,
)

from core_entity_django.services.wip_transfer_service import (
    transfer_wip_to_assets,
)

from core_entity_django.services.asset_export_service import (
    export_xlsx,
    export_pdf,
)


def _request_context(request):
    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    source_ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else request.META.get("REMOTE_ADDR")
    )

    device = request.META.get(
        "HTTP_USER_AGENT",
        "",
    )

    return source_ip, device


def _get_request_user(request):
    """
    Development/testing helper.

    If the request is authenticated, use the real request user.

    If authentication is disabled for testing and request.user
    is AnonymousUser, use the existing Django User with id=1.

    Current development user:
        id=1
        username=hsuthazin
    """

    User = get_user_model()

    if request.user and request.user.is_authenticated:
        return request.user

    return User.objects.get(id=1)


class AssetListCreateView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def get(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "view",
        )

        filters = {
            "draft_date_from": request.query_params.get(
                "draft_date_from"
            ),
            "draft_date_to": request.query_params.get(
                "draft_date_to"
            ),
            "acquisition_date_from": request.query_params.get(
                "acquisition_date_from"
            ),
            "acquisition_date_to": request.query_params.get(
                "acquisition_date_to"
            ),
            "asset_class": request.query_params.get(
                "asset_class"
            ),
            "asset_category": request.query_params.get(
                "asset_category"
            ),
            "asset_type": request.query_params.get(
                "asset_type"
            ),
            "source": request.query_params.get(
                "source"
            ),
            "company": request.query_params.get(
                "company"
            ),
            "branch": request.query_params.get(
                "branch"
            ),
            "department": request.query_params.get(
                "department"
            ),
            "supplier": request.query_params.get(
                "supplier"
            ),
            "validation_status": request.query_params.get(
                "validation_status"
            ),
            "capitalization_eligible": (
                request.query_params.get(
                    "capitalization_eligible"
                )
            ),
            "prepared_by": request.query_params.get(
                "prepared_by"
            ),
            "import_batch": request.query_params.get(
                "import_batch"
            ),
            "wip_reference": request.query_params.get(
                "wip_reference"
            ),
            "keyword": request.query_params.get(
                "keyword"
            ),
        }

        if (
            filters["capitalization_eligible"]
            in (None, "")
        ):
            filters["capitalization_eligible"] = None
        else:
            filters["capitalization_eligible"] = (
                filters["capitalization_eligible"].lower()
                == "true"
            )

        filters = {
            key: value
            for key, value in filters.items()
            if value not in (
                None,
                "",
            )
        }

        queryset = list_draft_assets(
            filters
        )

        return Response(
            AssetCoreSerializer(
                queryset,
                many=True,
            ).data
        )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "create",
        )

        serializer = AssetCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        source_ip, device = _request_context(
            request
        )

        asset = create_asset(
            user=user,
            validated_data=serializer.validated_data,
            source_ip=source_ip,
            device=device,
        )

        return Response(
            AssetCoreSerializer(asset).data,
            status=status.HTTP_201_CREATED,
        )


class AssetDetailView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def get(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "view",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            AssetCoreSerializer(asset).data
        )

    def put(self, request, pk):
        return self._update(request, pk)

    def patch(self, request, pk):
        return self._update(request, pk)

    def _update(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "edit",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AssetUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        source_ip, device = _request_context(
            request
        )

        try:
            asset = update_asset(
                asset=asset,
                user=user,
                validated_data=serializer.validated_data,
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            AssetCoreSerializer(asset).data
        )

    def delete(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "delete",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DeleteAssetSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        source_ip, device = _request_context(
            request
        )

        try:
            delete_asset(
                asset=asset,
                user=user,
                reason=serializer.validated_data["reason"],
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "detail": (
                "Draft asset deleted successfully."
            )
        })


class AssetValidateView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "validate",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        source_ip, device = _request_context(
            request
        )

        try:
            result = validate_asset(
                asset=asset,
                user=user,
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "asset": AssetCoreSerializer(
                result["asset"]
            ).data,
            "errors": result["errors"],
            "warnings": result["warnings"],
        })


class BulkValidateView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "bulk_validate",
        )

        serializer = BulkAssetSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assets = list_draft_assets().filter(
            id__in=serializer.validated_data[
                "asset_ids"
            ]
        )

        source_ip, device = _request_context(
            request
        )

        results = bulk_validate(
            assets=assets,
            user=user,
            source_ip=source_ip,
            device=device,
        )

        return Response({
            "results": results
        })


class AssetCapitalizeView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "capitalize",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        source_ip, device = _request_context(
            request
        )

        try:
            capitalization = capitalize_asset(
                asset=asset,
                user=user,
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "detail": (
                "Asset has been capitalized successfully."
            ),
            "transaction_reference": (
                capitalization.transaction_reference
            ),
            "asset_id": capitalization.asset_id,
        })


class BulkCapitalizeView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "bulk_capitalize",
        )

        serializer = BulkCapitalizeSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assets = get_capitalization_candidates(
            serializer.validated_data["asset_ids"]
        )

        source_ip, device = _request_context(
            request
        )

        results = []

        for asset in assets:

            try:

                capitalization = capitalize_asset(
                    asset=asset,
                    user=user,
                    source_ip=source_ip,
                    device=device,
                )

                results.append({
                    "asset_id": asset.id,
                    "status": "CAPITALIZED",
                    "transaction_reference": (
                        capitalization.transaction_reference
                    ),
                })

            except ValidationError as exc:

                results.append({
                    "asset_id": asset.id,
                    "status": "ERROR",
                    "errors": exc.messages,
                })

        return Response({
            "results": results
        })


class BulkDeleteView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "bulk_delete",
        )

        serializer = BulkDeleteSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assets = list_draft_assets().filter(
            id__in=serializer.validated_data[
                "asset_ids"
            ]
        )

        source_ip, device = _request_context(
            request
        )

        results = bulk_delete(
            assets=assets,
            user=user,
            reason=serializer.validated_data["reason"],
            source_ip=source_ip,
            device=device,
        )

        return Response({
            "results": results
        })


class AssetApprovalPdfView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def get(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "print",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        source_ip, device = _request_context(
            request
        )

        return generate_approval_pdf(
            asset=asset,
            user=user,
            source_ip=source_ip,
            device=device,
        )


class BulkApprovalPdfView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "print",
        )

        serializer = BulkAssetSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        assets = list_draft_assets().filter(
            id__in=serializer.validated_data[
                "asset_ids"
            ]
        )

        source_ip, device = _request_context(
            request
        )

        return generate_bulk_approval_pdf(
            assets=assets,
            user=user,
            source_ip=source_ip,
            device=device,
        )


class AssetApprovalActionView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "approve",
        )

        serializer = ApprovalActionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        source_ip, device = _request_context(
            request
        )

        try:
            asset = approval_action(
                asset=asset,
                user=user,
                action=serializer.validated_data["action"],
                reason=serializer.validated_data.get(
                    "reason",
                    "",
                ),
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            AssetCoreSerializer(asset).data
        )


class AssetDocumentListCreateView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "view",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            AssetDocumentSerializer(
                asset.documents.all(),
                many=True,
            ).data
        )

    def post(self, request, pk):

        user = _get_request_user(request)

        require_permission(
            user,
            "edit",
        )

        asset = get_asset(pk)

        if not asset:
            return Response(
                {"detail": "Asset not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AssetDocumentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        document = serializer.save(
            asset=asset,
            uploaded_by=user,
        )

        return Response(
            AssetDocumentSerializer(document).data,
            status=status.HTTP_201_CREATED,
        )


class AssetImportView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "import",
        )

        serializer = ImportAssetSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        source_ip, device = _request_context(
            request
        )

        result = import_assets(
            user=user,
            uploaded_file=serializer.validated_data[
                "file"
            ],
            template_version=serializer.validated_data[
                "template_version"
            ],
            source_ip=source_ip,
            device=device,
        )

        return Response({
            "batch_number": (
                result["batch"].batch_number
            ),
            "status": result["batch"].status,
            "total_rows": result["batch"].total_rows,
            "valid_rows": result["batch"].valid_rows,
            "error_rows": result["batch"].error_rows,
            "errors": result["errors"],
        })


class WipTransferView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def post(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "wip_transfer",
        )

        serializer = WipTransferSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        source_ip, device = _request_context(
            request
        )

        try:
            result = transfer_wip_to_assets(
                user=user,
                validated_data=serializer.validated_data,
                source_ip=source_ip,
                device=device,
            )

        except ValidationError as exc:
            return Response(
                {"detail": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "created_asset_ids": [
                asset.id
                for asset in result["assets"]
            ],
            "total_allocated": str(
                result["total_allocated"]
            ),
            "remaining_balance": str(
                result["remaining_balance"]
            ),
        }, status=status.HTTP_201_CREATED)


class AssetExportView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    permission_classes = (
        [AllowAny]
        if getattr(
            settings,
            "FAR_DISABLE_AUTH_FOR_TESTING",
            False,
        )
        else [IsAuthenticated]
    )

    def get(self, request):

        user = _get_request_user(request)

        require_permission(
            user,
            "export",
        )

        filters = {
            key: request.query_params.get(key)
            for key in [
                "draft_date_from",
                "draft_date_to",
                "acquisition_date_from",
                "acquisition_date_to",
                "asset_class",
                "asset_category",
                "asset_type",
                "source",
                "company",
                "branch",
                "department",
                "supplier",
                "validation_status",
                "keyword",
            ]
        }

        filters = {
            key: value
            for key, value in filters.items()
            if value not in (
                None,
                "",
            )
        }

        queryset = list_draft_assets(
            filters
        )

        export_format = request.query_params.get(
            "format",
            "xlsx",
        ).lower()

        if export_format == "pdf":
            return export_pdf(queryset)

        return export_xlsx(queryset)
