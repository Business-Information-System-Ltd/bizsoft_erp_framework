from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core_entity_django.models import (
    AssetAuditLog,
    AssetCore,
)


def _draw_label_value(pdf, y, label, value):
    pdf.drawString(
        50,
        y,
        f"{label}: {value or ''}",
    )
    return y - 18


def _draw_asset_page(pdf, asset, print_number):

    width, height = A4
    y = height - 45

    pdf.setFont(
        "Helvetica-Bold",
        15,
    )

    pdf.drawString(
        50,
        y,
        "ASSET CAPITALIZATION APPROVAL FORM",
    )

    y -= 28

    pdf.setFont(
        "Helvetica",
        9,
    )

    header_rows = [
        ("Company", getattr(
            getattr(asset, "location_info", None),
            "company_legal_entity",
            "",
        )),
        ("Document Title", "Asset Capitalization Approval Form"),
        ("Draft Asset Number", asset.draft_asset_number),
        ("Asset Code", asset.asset_code or ""),
        ("Print Date", str(timezone.localdate())),
        ("Print No.", str(print_number)),
        ("Source", asset.entry_source),
        ("Prepared By", asset.prepared_by.get_username()),
    ]

    for label, value in header_rows:
        y = _draw_label_value(
            pdf,
            y,
            label,
            value,
        )

    y -= 8
    pdf.line(50, y, width - 50, y)
    y -= 20

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "1. Asset Details",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    if hasattr(asset, "basic_info"):
        rows = [
            ("Asset Name", asset.basic_info.asset_name),
            ("Description", asset.basic_info.asset_description),
            ("Asset Type", asset.basic_info.asset_type),
            ("Brand / Model",
             f"{asset.basic_info.brand} / {asset.basic_info.model}"),
            ("Serial Number", asset.basic_info.serial_number),
            ("Quantity", str(asset.basic_info.quantity)),
            ("Unit", asset.basic_info.unit_of_measure),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    y -= 8
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "2. Classification",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    if hasattr(asset, "classification"):
        rows = [
            ("Asset Class", asset.classification.asset_class),
            ("Asset Category", asset.classification.asset_category),
            ("Sub-Category", asset.classification.asset_subcategory),
            ("Depreciation Method",
             asset.classification.depreciation_method),
            ("Useful Life",
             str(asset.classification.useful_life or "")),
            ("Residual Value",
             str(asset.classification.residual_value or "")),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    y -= 8
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "3. Financial Information",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    if hasattr(asset, "financial_info"):
        rows = [
            ("Acquisition Date",
             str(asset.financial_info.acquisition_date or "")),
            ("Invoice Number",
             asset.financial_info.invoice_number),
            ("Supplier",
             getattr(
                 getattr(asset, "supplier_info", None),
                 "supplier_name",
                 "",
             )),
            ("Purchase Cost",
             str(asset.financial_info.purchase_cost)),
            ("Other Direct Cost",
             str(asset.financial_info.other_directly_attributable_cost)),
            ("Total Capitalizable Cost",
             str(asset.financial_info.total_capitalizable_cost)),
            ("Currency",
             asset.financial_info.currency),
            ("Exchange Rate",
             str(asset.financial_info.exchange_rate or "")),
            ("Functional Currency Amount",
             str(asset.financial_info.functional_currency_amount or "")),
            ("Proposed Capitalization Date",
             str(asset.financial_info.capitalization_date or "")),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    if y < 220:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "4. Accounting Information",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    if hasattr(asset, "financial_info"):
        rows = [
            ("GL Asset Account",
             asset.financial_info.gl_asset_account),
            ("Accumulated Depreciation Account",
             asset.financial_info.accumulated_depreciation_account),
            ("Depreciation Expense Account",
             asset.financial_info.depreciation_expense_account),
            ("Cost Center",
             asset.financial_info.cost_center),
            ("Funding Source",
             asset.financial_info.funding_source),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    y -= 8
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "5. Location and Custodian",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    if hasattr(asset, "location_info"):
        rows = [
            ("Company / Branch",
             f"{asset.location_info.company_legal_entity} / "
             f"{asset.location_info.branch}"),
            ("Department",
             asset.location_info.department),
            ("Location",
             asset.location_info.location),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    if hasattr(asset, "responsibility"):
        rows = [
            ("Custodian",
             asset.responsibility.custodian_employee),
            ("User Department",
             asset.responsibility.user_department),
            ("Assigned User",
             asset.responsibility.assigned_user),
        ]

        for label, value in rows:
            y = _draw_label_value(
                pdf,
                y,
                label,
                value,
            )

    y -= 10

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "6. Supporting Documents Checklist",
    )

    y -= 20
    pdf.setFont("Helvetica", 9)

    document_types = {
        "INVOICE": "Supplier Invoice",
        "PURCHASE_ORDER": "Purchase Order",
        "DELIVERY_NOTE": "Delivery Note",
        "APPROVAL": "Management Approval",
        "WIP_COMPLETION": "WIP Completion Report",
        "OTHER": "Other Supporting Documents",
    }

    existing_types = set(
        asset.documents.values_list(
            "document_type",
            flat=True,
        )
    )

    for key, label in document_types.items():
        mark = "YES" if key in existing_types else "NO"
        y = _draw_label_value(
            pdf,
            y,
            label,
            mark,
        )

    if y < 180:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        50,
        y,
        "7. Approval",
    )

    y -= 35
    pdf.setFont("Helvetica", 9)

    for title in [
        "Prepared By",
        "Reviewed By - Finance",
        "Reviewed By - Admin / Asset Controller",
        "Approved By - Department Head",
        "Approved By - Management",
    ]:
        pdf.drawString(
            50,
            y,
            f"{title}: ______________________________",
        )

        y -= 28

    if print_number > 1:
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(
            50,
            y,
            f"REPRINT - COPY #{print_number}",
        )


def _mark_printed(
    *,
    asset,
    user,
    source_ip=None,
    device="",
):
    asset.approval_print_count += 1
    asset.last_printed_at = timezone.now()
    asset.last_printed_by = user

    if asset.approval_status == AssetCore.ApprovalStatus.NOT_SUBMITTED:
        asset.approval_status = (
            AssetCore.ApprovalStatus.PRINTED
        )

    asset.save(
        update_fields=[
            "approval_status",
            "approval_print_count",
            "last_printed_at",
            "last_printed_by",
            "last_updated_date",
        ]
    )

    AssetAuditLog.objects.create(
        asset=asset,
        action_type=AssetAuditLog.ActionType.PRINT,
        user=user,
        new_value={
            "approval_status": asset.approval_status,
            "print_count": asset.approval_print_count,
        },
        source_ip=source_ip,
        device=device,
    )


def generate_approval_pdf(
    *,
    asset,
    user,
    source_ip=None,
    device="",
):

    if asset.is_deleted:
        raise ValidationError(
            "Deleted asset cannot be printed."
        )

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    _draw_asset_page(
        pdf,
        asset,
        asset.approval_print_count + 1,
    )

    pdf.save()
    buffer.seek(0)

    _mark_printed(
        asset=asset,
        user=user,
        source_ip=source_ip,
        device=device,
    )

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=(
            f"{asset.draft_asset_number}_approval.pdf"
        ),
        content_type="application/pdf",
    )


def generate_bulk_approval_pdf(
    *,
    assets,
    user,
    source_ip=None,
    device="",
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    for asset in assets:

        if asset.is_deleted:
            continue

        _draw_asset_page(
            pdf,
            asset,
            asset.approval_print_count + 1,
        )

        pdf.showPage()

        _mark_printed(
            asset=asset,
            user=user,
            source_ip=source_ip,
            device=device,
        )

    pdf.save()
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="FAR_Bulk_Approval_Documents.pdf",
        content_type="application/pdf",
    )