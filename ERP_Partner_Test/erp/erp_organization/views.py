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
Defines simple DRF API views for organization data.
"""


try:
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from django.db.models import Q
    from rest_framework import status
    from rest_framework.generics import ListAPIView
    from erp_organization.constants import PhysicalLocationType
    from erp_organization.models import *
    from erp_organization.serializers import *
    from reportlab.pdfgen import canvas
    from django.http import HttpResponse
    from django.db import transaction
    from rest_framework.generics import ListCreateAPIView
    from rest_framework.decorators import api_view
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
    )
    from erp_organization.services.legal_entity_application_service import LegalEntityApplicationService
    from erp_organization.services.branch_application_service import BranchApplicationService
    from erp_organization.repositories.branch_repository import BranchRepository
    from erp_organization.services.address_application_service import AddressApplicationService
    from erp_organization.services.zone_application_service import ZoneApplicationService
    from erp_organization.services.region_application_service import RegionApplicationService
    from erp_organization.services.department_application_service import DepartmentApplicationService
    from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService
    from erp_organization.services.location_type_services import LocationTypeService
    from erp_organization.services.hierarchy_service import OrganizationHierarchyService
    class OrganizationUnitListView(ListCreateAPIView): queryset=OrganizationUnit.objects.filter(is_active=True); serializer_class=OrganizationUnitSerializer
    # class LegalEntityListCreateView(APIView):

    #     def get(self, request):
    #         """
    #         Get active legal entities.
    #         """
    #         # is_active = request.query_params.get("is_active")
    #         # country_code = request.query_params.get("country_code")
            
    #         # search = request.query_params.get("search")
    #         legal_entities = LegalEntityProfile.objects.filter(
    #             is_active=True
    #         )

    #         # if is_active:
    #         #     if is_active.upper() == "ACTIVE":
    #         #         legal_entities = legal_entities.filter(is_active=True)
    #         #     elif is_active.upper() == "INACTIVE":
    #         #         legal_entities = legal_entities.filter(is_active=False)
    #         # if country_code:
    #         #     legal_entities = legal_entities.filter(
    #         #         country_code=country_code
    #         #         )
               
    #         # if search:
    #         #     legal_entities = legal_entities.filter(
    #         #         Q(legal_entity_code__icontains=search) |
    #         #         Q(legal_entity_name__icontains=search) |
    #         #         Q(registration_no__icontains=search) |
    #         #         Q(tax_registration_no__icontains=search) |
    #         #         Q(functional_currency_code__icontains=search) |
    #         #         Q(presentation_currency_code__icontains=search)
    #         #     )
    #         serializer = LegalEntityProfileSerializer(
    #             legal_entities,
    #             many=True
    #         )

    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )

    #     def post(self, request):
    #         legal_entity =LegalEntityApplicationService.create_legal_entity(
    #             user=request.user,
    #             data=request.data
    #         )

    #         # legal_entity = LegalEntityApplicationService.create_legal_entity(
    #         #     user=request.user,
    #         #     data=request.data
    #         # )

    #         serializer = LegalEntityProfileSerializer(
    #             legal_entity
    #         )

    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED
    #         )
    # class LegalEntityListView(ListAPIView): queryset=LegalEntityProfile.objects.filter(is_active=True); serializer_class=LegalEntityProfileSerializer
    # class BranchListView(ListAPIView): queryset=BranchProfile.objects.filter(is_active=True); serializer_class=BranchProfileSerializer



    class LegalEntityListCreateView(APIView):
        
            def get(self, request):
                """
                Get active legal entities.
                """
                legal_entities = LegalEntityProfile.objects.filter(
                    is_active=True
                )
                
                filters = {
                    "is_active": request.query_params.get("is_active"),
                    "legal_entity_code": request.query_params.get("legal_entity_code"),
                    "legal_entity_name": request.query_params.get("legal_entity_name"),
                    "country_code": request.query_params.get("country_code"),
                    "legal_form": request.query_params.get("legal_form"),
                    "registration_no": request.query_params.get("registration_no"),
                    "tax_registration_no": request.query_params.get("tax_registration_no"),
                    "functional_currency_code": request.query_params.get("functional_currency"),
                    "presentation_currency_code": request.query_params.get("presentation_currency_code"),
                    "financial_year_start_month": request.query_params.get("financial_year_start_month"),
                    "financial_year_start_day": request.query_params.get("financial_year_start_day"),
                    "search": request.query_params.get("search"),
                }

                

                LegalEntities = (
                    LegalEntityApplicationService.get_filtered_legal_entities(filters)
                )
                serializer = LegalEntityProfileSerializer(
                    LegalEntities,
                    many=True
                )
    
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
    
            def post(self, request):
                legal_entity =LegalEntityApplicationService.create_legal_entity(
                    user=request.user,
                    data=request.data
                )
    
                serializer = LegalEntityProfileSerializer(
                    legal_entity
                )
    
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

    class LegalEntityPDFExportView(APIView):

        def get(self, request):

            filters = {
                "is_active": request.query_params.get("is_active"),
                "legal_entity_code": request.query_params.get("legal_entity_code"),
                "legal_entity_name": request.query_params.get("legal_entity_name"),
                "country_code": request.query_params.get("country_code"),
                "legal_form": request.query_params.get("legal_form"),
                "registration_no": request.query_params.get("registration_no"),
                "tax_registration_no": request.query_params.get("tax_registration_no"),
                "functional_currency_code": request.query_params.get("functional_currency_code"),
                "presentation_currency_code": request.query_params.get("presentation_currency_code"),
                "financial_year_start_month": request.query_params.get("financial_year_start_month"),
                "financial_year_start_day": request.query_params.get("financial_year_start_day"),
                "search": request.query_params.get("search"),
            }

            legal_entities = LegalEntityApplicationService.get_filtered_legal_entities(
                filters
            )

            response = HttpResponse(
                content_type="application/pdf"
            )

            response["Content-Disposition"] = (
                'attachment; filename="legal_entity_list.pdf"'
            )

            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(A4)
            )

            styles = getSampleStyleSheet()

            elements = []

            
            title = Paragraph(
                "<b>Legal Entity List Report</b>",
                styles["Title"]
            )

            elements.append(title)
            elements.append(Spacer(1, 12))

            
            data = [[
                "Legal\nEntity\nCode",
                "Legal\nEntity\nName",
                "Country\nCode",
                "Legal\nForm",
                "Registration\nNo",
                "Tax\nRegistration\nNo",
                "Functional\nCurrency",
                "Presentation\nCurrency",
                "Financial\nYear\nStart\nMonth",
                "Financial\nYear\nStart\nDay",
                "Status"
            ]]

            
            
            for legal_entity in legal_entities:

                data.append([
                    legal_entity.legal_entity_code,
                    legal_entity.legal_entity_name,
                    legal_entity.country_code or "",
                    legal_entity.legal_form or "",
                    legal_entity.registration_no or "",
                    legal_entity.tax_registration_no or "",
                    legal_entity.functional_currency_code or "",
                    legal_entity.presentation_currency_code or "",
                    legal_entity.financial_year_start_month or "",
                    legal_entity.financial_year_start_day or "",
                    "Active" if legal_entity.is_active else "Inactive",
                    
                ])

            
            table = Table(
                data,
                colWidths=[
                    70,     # Legal Entity Code
                    130,    # Legal Entity Name
                    40,     # Country Code
                    80,     # Legal Form
                    80,     # Registration No
                    70,     # Tax Registration No
                    60,     # Functional Currency
                    60,     # Presentation Currency
                    50,     # Financial Year Start Month
                    50,     # Financial Year Start Day
                    40,     # Status
                  
                ]
            )

            
            table.setStyle(TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, -1), 9),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("ALIGN", (0, 1), (-1, -1), "LEFT"),


                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ]))

            elements.append(table)

            doc.build(elements)

            return response
    class RegionListView(APIView):
        def get(self, request):
            filters = {
                "is_active": request.query_params.get("is_active"),
                "region_code": request.query_params.get("region_code"),
                "search": request.query_params.get("search"),
            }
            regions = RegionApplicationService.get_filtered_regions(filters)
            return Response(RegionSerializer(regions, many=True).data, status=status.HTTP_200_OK)
    
        def post(self, request):
            region = RegionApplicationService.create_region(request.data)
            return Response(RegionSerializer(region).data, status=status.HTTP_201_CREATED)


    class RegionDetailView(APIView):
        def get_object(self, region_id):
            return Region.objects.filter(pk=region_id).first()

        def delete(self, request, region_id):

            region = self.get_object(region_id)

            if not region:
                return Response(
                    {"detail": "Region not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            region.delete()

            return Response(
                {"detail": "Region deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

    class ZoneListView(APIView):
        def get(self, request):
            filters = {
                "region": request.query_params.get("region", request.query_params.get("region_id")),
                "zone_code": request.query_params.get("zone_code"),
                "is_active": request.query_params.get("is_active"),
                "search": request.query_params.get("search"),
            }
            zones = ZoneApplicationService.get_filtered_zones(filters)
            return Response(ZoneSerializer(zones, many=True).data, status=status.HTTP_200_OK)

        def post(self, request):
            zone = ZoneApplicationService.create_zone(request.data)
            return Response(ZoneSerializer(zone).data, status=status.HTTP_201_CREATED)
    class ZoneDetailView(APIView):
        def get_object(self, zone_id):
            return Zone.objects.filter(pk=zone_id).first()

        def delete(self, request, zone_id):

            zone = self.get_object(zone_id)

            if not zone:
                return Response(
                    {"detail": "Zone not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            zone.delete()

            return Response(
                {"detail": "Zone deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

    class AddressListView(APIView):
        def get(self, request):
            filters = {
                "region": request.query_params.get("region", request.query_params.get("region_id")),
                "zone": request.query_params.get("zone", request.query_params.get("zone_id")),
                "city": request.query_params.get("city"),
                "township": request.query_params.get("township"),
                "is_active": request.query_params.get("is_active"),
                "search": request.query_params.get("search"),
            }
            addresses = AddressApplicationService.get_filtered_addresses(filters)
            return Response(AddressSerializer(addresses, many=True).data, status=status.HTTP_200_OK)

        def post(self, request):
            address = AddressApplicationService.create_address(request.data)
            return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)

        
        


    class AddressDetailView(APIView):

        def get(self, request, address_id):
            try:
                address = AddressApplicationService.get_address(
                    address_id
                )

                return Response(
                    AddressSerializer(address).data,
                    status=status.HTTP_200_OK,
                )

            except Address.DoesNotExist:
                return Response(
                    {
                        "detail": "Address not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        def put(self, request, address_id):
            try:
                address = AddressApplicationService.update_address(
                    address_id,
                    request.data,
                )

                return Response(
                    AddressSerializer(address).data,
                    status=status.HTTP_200_OK,
                )

            except Address.DoesNotExist:
                return Response(
                    {
                        "detail": "Address not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        def patch(self, request, address_id):
            try:
                address = AddressApplicationService.update_address(
                    address_id,
                    request.data,
                )

                return Response(
                    AddressSerializer(address).data,
                    status=status.HTTP_200_OK,
                )

            except Address.DoesNotExist:
                return Response(
                    {
                        "detail": "Address not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        def get_object(self, address_id):
            return Address.objects.filter(pk=address_id).first()
        
        def delete(self, request, address_id):
    
                address = self.get_object(address_id)
    
                if not address:
                    return Response(
                        {"detail": "Address not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
    
                address.delete()
    
                return Response(
                    {"detail": "Address deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
    class BranchListCreateView(APIView):
        def get(self, request):
            filters = {
                "is_active": request.query_params.get("is_active"),
                "region": request.query_params.get("region"),
                "zone": request.query_params.get("zone"),
                "legal_entity": request.query_params.get("legal_entity"),
                "branch_type": request.query_params.get("branch_type"),
                "search": request.query_params.get("search"),
            }
            branches = BranchApplicationService.get_filtered_branches(filters)
            return Response(BranchProfileSerializer(branches, many=True).data, status=status.HTTP_200_OK)

        def post(self, request):
            branch = BranchApplicationService.create_branch(user=request.user, data=request.data)
            return Response(BranchProfileSerializer(branch).data, status=status.HTTP_201_CREATED)

    class BranchDetailView(APIView):
        def get_object(self, branch_id):
            return BranchRepository().get_by_id(branch_id)

        def get(self, request, branch_id):
            branch = self.get_object(branch_id)
            if not branch:
                return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(BranchProfileSerializer(branch).data, status=status.HTTP_200_OK)

        def put(self, request, branch_id):
            branch = BranchApplicationService.update_branch(branch_id=branch_id, user=request.user, data=request.data)
            return Response(BranchProfileSerializer(branch).data, status=status.HTTP_200_OK)

        def patch(self, request, branch_id):
            branch = BranchApplicationService.update_branch(branch_id=branch_id, user=request.user, data=request.data)
            return Response(BranchProfileSerializer(branch).data, status=status.HTTP_200_OK)

        def delete(self, request, branch_id):
            branch = self.get_object(branch_id)
            if not branch:
                return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)
            branch.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    class BranchPDFExportView(APIView):

        def get(self, request):

           
            filters = {
                "is_active": request.query_params.get("is_active"),
                "region": request.query_params.get("region"),
                "zone": request.query_params.get("zone"),
                "legal_entity": request.query_params.get("legal_entity"),
                "branch_type": request.query_params.get("branch_type"),
                "search": request.query_params.get("search"),
            }

            branches = BranchApplicationService.get_filtered_branches(
                filters
            )

           
            response = HttpResponse(
                content_type="application/pdf"
            )

            response["Content-Disposition"] = (
                'attachment; filename="branch_list.pdf"'
            )

            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(A4),
                rightMargin=20,
                leftMargin=20,
                topMargin=20,
                bottomMargin=20,
            )

            styles = getSampleStyleSheet()

            elements = []


            title = Paragraph(
                "<b>Branch List Report</b>",
                styles["Title"],
            )

            elements.append(title)
            elements.append(Spacer(1, 12))


            data = [[
                "No",
                "Branch\nCode",
                "Branch\nName",
                "Legal\nEntity",
                "Branch\nType",
                "Region",
                "Zone",
                # "Address",
                # "Latitude",
                # "Longitude",
                "Head\nOffice",
                "Bank\nBranch",
                "Cost\nCenter",
                "Profit\nCenter",
                "Inventory\nStorable",
                "Asset\nAssignable",
                "Effective\nFrom",
                "Effective\nTo",
                "Status",
            ]]

            for index, branch in enumerate(branches, start=1):

                organization_unit = branch.organization_unit

                # address = branch.address

                # address_text = ""

                # if address:

                #     address_parts = []

                #     if address.address_line_1:
                #         address_parts.append(
                #             address.address_line_1
                #         )

                #     if address.address_line_2:
                #         address_parts.append(
                #             address.address_line_2
                #         )

                #     if address.township:
                #         address_parts.append(
                #             address.township
                #         )

                #     # if address.city:
                #     #     address_parts.append(
                #     #         address.city
                #     #     )

                #     # if address.postal_code:
                #     #     address_parts.append(
                #     #         address.postal_code
                #     #     )

                #     address_text = ", ".join(
                #         address_parts
                #     )

                effective_from = (
                    organization_unit.effective_from
                )

                effective_to = (
                    organization_unit.effective_to
                )

                data.append([
                    index,
                    # Branch
                    branch.branch_code or "",

                    branch.branch_name or "",

                    # Legal Entity
                    getattr(
                        branch.legal_entity,
                        "legal_entity_name",
                        "",
                    ),

                    # Branch Type
                    branch.branch_type or "",

                    # Region
                    getattr(
                        branch.region,
                        "region_code",
                        "",
                    ),

                    # Zone
                    getattr(
                        branch.zone,
                        "zone_code",
                        "",
                    ),

                    # # Address
                    # address_text,

                    # # Location
                    # str(branch.latitude)
                    # if branch.latitude is not None
                    # else "",

                    # str(branch.longitude)
                    # if branch.longitude is not None
                    # else "",

                    # Responsibility
                    "Yes"
                    if branch.is_head_office
                    else "No",

                    "Yes"
                    if branch.is_bank_branch
                    else "No",

                    "Yes"
                    if organization_unit.is_cost_center
                    else "No",

                    "Yes"
                    if organization_unit.is_profit_center
                    else "No",

                    "Yes"
                    if organization_unit.is_inventory_storable
                    else "No",

                    "Yes"
                    if organization_unit.is_asset_assignable
                    else "No",

                   

                    # Effective Dates
                    effective_from.strftime("%Y-%m-%d")
                    if effective_from
                    else "",

                    effective_to.strftime("%Y-%m-%d")
                    if effective_to
                    else "",

                # Status
                    "Active"
                    if branch.is_active
                    else "Inactive",
                ])


            table = Table(
                data,
                repeatRows=1,
                colWidths=[
                    20,
                    60,   # Branch Code
                    80,   # Branch Name
                    90,  # Legal Entity
                    70,   # Branch Type
                    55,   # Region
                    55,   # Zone
                    # 120,  # Address
                    # 40,   # Latitude
                    # 40,   # Longitude
                    40,   # Head Office
                    40,   # Bank Branch
                    40,   # Cost Center
                    40,   # Profit Center
                    40,   # Inventory
                    40,   # Asset
                    50,   # Effective From
                    50,   # Effective To
                    40,   # Status
                ],
            )

            table.setStyle(
                TableStyle([

                    # Border
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black,
                    ),

                    # Header
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),

                    (
                        "ALIGN",
                        (0, 0),
                        (-1, 0),
                        "CENTER",
                    ),

                    (
                        "ALIGN",
                        (7, 1),
                        (17, -1),
                        "CENTER",
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        6,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, 0),
                        6,
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ])
            )

            elements.append(table)

           
            doc.build(elements)

            return response


    class DepartmentListCreateView(APIView):
        
        def get(self, request):
            """
            Get active department profiles.
            """
            department_profiles = DepartmentProfile.objects.filter(
                is_active=True
            )
            
            filters = {
                "is_active": request.query_params.get("is_active"),
                "department_code": request.query_params.get("department_code"),
                "department_name": request.query_params.get("department_name"),
                "branch": request.query_params.get("branch"),
                "legal_entity": request.query_params.get("legal_entity"),
                "parent_department": request.query_params.get("parent_department"),
                "search": request.query_params.get("search"),
            }

            department_profiles = (
                DepartmentApplicationService.get_filtered_departments(filters)
            )
            serializer = DepartmentProfileSerializer(
                department_profiles,
                many=True
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        def post(self, request):
            department = DepartmentApplicationService.create_department(
                user=request.user,
                data=request.data
            )

            serializer = DepartmentProfileSerializer(
                department
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
                    
    
    class DepartmentPDFExportView(APIView):
    
        def get(self, request):

            filters = {
                "is_active": request.query_params.get("is_active"),
                "department_code": request.query_params.get("department_code"),
                "department_name": request.query_params.get("department_name"),
                "branch": request.query_params.get("branch"),
                "legal_entity": request.query_params.get("legal_entity"),
                "parent_department": request.query_params.get("parent_department"),
                "search": request.query_params.get("search"),
            }

            departments = DepartmentApplicationService.get_filtered_departments(
                filters
            )

            response = HttpResponse(
                content_type="application/pdf"
            )

            response["Content-Disposition"] = (
                'attachment; filename="department_list.pdf"'
            )

            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(A4)
            )

            styles = getSampleStyleSheet()

            elements = []

            
            title = Paragraph(
                "<b>Department List Report</b>",
                styles["Title"]
            )

            elements.append(title)
            elements.append(Spacer(1, 12))

            
            data = [[
                "Department\nCode",
                "Department Name",
                "Legal Entity",
                "Branch",
                "Parent\nDepartment",
                "Status"
            ]]

            
            
            for department in departments:

                data.append([
                    department.department_code,
                    department.department_name,
                    getattr(
                        department.legal_entity,
                        "legal_entity_name",
                        ""
                    ),
                    getattr(
                        department.branch,
                        "branch_name",
                        ""
                    ),
                    getattr(
                        department.parent_department,
                        "department_name",
                        ""
                    ),
                    "Active" if department.is_active else "Inactive",
                ])

            
            table = Table(
                data,
                colWidths=[
                    70,     # Department Code
                    130,    # Department Name
                    130,    # Legal Entity
                    110,     # Branch 
                    110,     # Parent Department
                    40,     # Status
                ]
            )

            
            table.setStyle(TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, -1), 9),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("ALIGN", (0, 1), (-1, -1), "LEFT"),


                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ]))

            elements.append(table)

            doc.build(elements)

            return response
    # class DepartmentListView(ListAPIView): queryset=DepartmentProfile.objects.filter(is_active=True); serializer_class=DepartmentProfileSerializer
    class CostCenterListView(ListAPIView): queryset=CostCenterProfile.objects.filter(is_active=True); serializer_class=CostCenterProfileSerializer
    class ProfitCenterListView(ListAPIView): queryset=ProfitCenterProfile.objects.filter(is_active=True); serializer_class=ProfitCenterProfileSerializer
    # class PhysicalLocationListView(ListAPIView): queryset=PhysicalLocationProfile.objects.filter(is_active=True); serializer_class=PhysicalLocationProfileSerializer
    class PhysicalLocationListCreateView(APIView):
            
            def get(self, request):
                """
                Get active physical location profiles.
                """
                physical_location_profiles = PhysicalLocationProfile.objects.filter(
                    is_active=True
                )
                
                filters = {
                    "is_active": request.query_params.get("is_active"),
                    "location_code": request.query_params.get("location_code"),
                    "location_name": request.query_params.get("location_name"),
                    "location_type": request.query_params.get("location_type"),
                    "legal_entity": request.query_params.get("legal_entity"),
                    "responsible_department": request.query_params.get("responsible_department"),
                    "responsible_branch": request.query_params.get("responsible_branch"),
                    "search": request.query_params.get("search"),
                }
    
                physical_location_profiles = (
                    PhysicalLocationApplicationService.get_filtered_physical_locations(filters)
                )
                serializer = PhysicalLocationProfileSerializer(
                    physical_location_profiles,
                    many=True
                )
    
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
    
            def post(self, request):
                physical_location = PhysicalLocationApplicationService.create_physical_location(
                    user=request.user,
                    data=request.data
                )
    
                serializer = PhysicalLocationProfileSerializer(
                    physical_location
                )
    
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

    class PhysicalLocationPDFExportView(APIView):
        
        def get(self, request):

            filters = {
                "is_active": request.query_params.get("is_active"),
                "location_code": request.query_params.get("location_code"),
                "location_name": request.query_params.get("location_name"),
                "location_type": request.query_params.get("location_type"),
                "legal_entity": request.query_params.get("legal_entity"),
                "responsible_department": request.query_params.get("responsible_department"),
                "responsible_branch": request.query_params.get("responsible_branch"),
                "search": request.query_params.get("search"),
            }

            physical_locations = PhysicalLocationApplicationService.get_filtered_physical_locations(
                filters
            )

            response = HttpResponse(
                content_type="application/pdf"
            )

            response["Content-Disposition"] = (
                'attachment; filename="physical_location_list.pdf"'
            )

            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(A4)
            )

            styles = getSampleStyleSheet()

            elements = []

            
            title = Paragraph(
                "<b>Physical Location List Report</b>",
                styles["Title"]
            )

            elements.append(title)
            elements.append(Spacer(1, 12))

            
            data = [[
                "Location Code",
                "Location Name",
                "Location Type",
                "Legal Entity",
                "Branch",
                "Department",
                "Status"
            ]]

            
            
            for physical_location in physical_locations:

                data.append([
                    physical_location.location_code,
                    physical_location.location_name,
                    physical_location.location_type,
                    getattr(
                        physical_location.legal_entity,
                        "legal_entity_name",
                        ""
                    ),
                    getattr(
                        physical_location.responsible_branch,
                        "branch_name",
                        ""
                    ),
                    getattr(
                        physical_location.responsible_department,
                        "department_name",
                        ""
                    ),
                    "Active" if physical_location.is_active else "Inactive",
                ])

            
            table = Table(
                data,
                colWidths=[
                    70,     # Location Code
                    130,    # Location Name
                    130,    # Location Type
                    130,    # Legal Entity
                    110,     # Branch 
                    110,     # Parent Department
                    40,     # Status
                ]
            )

            
            table.setStyle(TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, -1), 9),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("ALIGN", (0, 1), (-1, -1), "LEFT"),


                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ]))

            elements.append(table)

            doc.build(elements)

            return response
    class OrganizationTreeView(APIView):
        def get(self,request): return Response(OrganizationHierarchyService.get_tree(unit_type=request.query_params.get('unit_type')))
    class BankBranchListView(ListAPIView): queryset=BranchProfile.objects.filter(is_bank_branch=True,is_active=True); serializer_class=BranchProfileSerializer
    class ATMLocationListView(ListAPIView): queryset=PhysicalLocationProfile.objects.filter(location_type=PhysicalLocationType.ATM_SITE,is_active=True); serializer_class=PhysicalLocationProfileSerializer
    class LocationTypeConfigAPIView(APIView):

        def get(
            self,
            request,
            location_type
        ):

            dynamic_fields = (
                LocationTypeService
                .get_dynamic_fields(
                    location_type
                )
            )


            if dynamic_fields is None:

                return Response(
                    {
                        "detail": (
                            "Location type "
                            "configuration not found"
                        )
                    },

                    status=status.HTTP_404_NOT_FOUND
                )


            return Response(
                dynamic_fields,
                status=status.HTTP_200_OK
            )
except Exception:
    OrganizationUnitListView=LegalEntityListView=BranchListView=DepartmentListView=CostCenterListView=ProfitCenterListView=PhysicalLocationListView=OrganizationTreeView=BankBranchListView=ATMLocationListView=None
