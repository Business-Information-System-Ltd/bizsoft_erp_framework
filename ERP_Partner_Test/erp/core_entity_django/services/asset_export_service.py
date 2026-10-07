from io import BytesIO

from django.http import FileResponse

from openpyxl import Workbook

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def export_xlsx(queryset):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Draft Assets"

    headers = [
        "Draft Asset Number",
        "Asset Code",
        "Asset Name",
        "Asset Class",
        "Asset Category",
        "Asset Type",
        "Source",
        "Draft Date",
        "Acquisition Date",
        "Supplier",
        "Invoice Number",
        "Purchase Cost",
        "Total Capitalizable Cost",
        "Currency",
        "Company",
        "Branch",
        "Department",
        "Validation Status",
        "Capitalization Eligibility",
        "Prepared By",
        "Last Updated",
    ]

    sheet.append(headers)

    for asset in queryset:

        sheet.append([
            asset.draft_asset_number,
            asset.asset_code or "",
            getattr(
                getattr(asset, "basic_info", None),
                "asset_name",
                "",
            ),
            getattr(
                getattr(asset, "classification", None),
                "asset_class",
                "",
            ),
            getattr(
                getattr(asset, "classification", None),
                "asset_category",
                "",
            ),
            getattr(
                getattr(asset, "basic_info", None),
                "asset_type",
                "",
            ),
            asset.entry_source,
            str(asset.draft_date),
            str(
                getattr(
                    getattr(asset, "financial_info", None),
                    "acquisition_date",
                    "",
                )
            ),
            getattr(
                getattr(asset, "supplier_info", None),
                "supplier_name",
                "",
            ),
            getattr(
                getattr(asset, "financial_info", None),
                "invoice_number",
                "",
            ),
            str(
                getattr(
                    getattr(asset, "financial_info", None),
                    "purchase_cost",
                    "",
                )
            ),
            str(
                getattr(
                    getattr(asset, "financial_info", None),
                    "total_capitalizable_cost",
                    "",
                )
            ),
            getattr(
                getattr(asset, "financial_info", None),
                "currency",
                "",
            ),
            getattr(
                getattr(asset, "location_info", None),
                "company_legal_entity",
                "",
            ),
            getattr(
                getattr(asset, "location_info", None),
                "branch",
                "",
            ),
            getattr(
                getattr(asset, "location_info", None),
                "department",
                "",
            ),
            asset.validation_status,
            "Yes" if asset.capitalization_eligible else "No",
            asset.prepared_by.get_username(),
            str(asset.last_updated_date),
        ])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="FAR_Draft_Assets.xlsx",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )


def export_pdf(queryset):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    width, height = A4
    y = height - 40

    pdf.setFont(
        "Helvetica-Bold",
        13,
    )

    pdf.drawString(
        40,
        y,
        "FAR Draft Asset List",
    )

    y -= 30
    pdf.setFont(
        "Helvetica",
        8,
    )

    for asset in queryset:

        line = (
            f"{asset.draft_asset_number} | "
            f"{getattr(getattr(asset, 'basic_info', None), 'asset_name', '')} | "
            f"{asset.entry_source} | "
            f"{asset.validation_status} | "
            f"{'Eligible' if asset.capitalization_eligible else 'Not Eligible'}"
        )

        pdf.drawString(
            40,
            y,
            line[:150],
        )

        y -= 15

        if y < 50:
            pdf.showPage()
            y = height - 40
            pdf.setFont(
                "Helvetica",
                8,
            )

    pdf.save()
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="FAR_Draft_Assets.pdf",
        content_type="application/pdf",
    )