from django.db import models


def choices(cls):
    return [(v, k.replace('_', ' ').title()) for k, v in cls.__dict__.items() if k.isupper() and isinstance(v, str)]

class LifecycleStatus(models.TextChoices):
    DRAFT='DRAFT', "Draft"; CAPITALIZED = "CAPITALIZED", "Capitalized"; COMMISSIONED = "COMMISSIONED", "Commissioned"; DECOMMISSIONED = "DECOMMISSIONED", "Decommissioned";DISPOSED = "DISPOSED", "Disposed"
LifecycleStatus.CHOICES=choices(LifecycleStatus)

class ValidationStatus(models.TextChoices):
    INCOMPLETE = "INCOMPLETE", "Incomplete";  COMPLETE = "COMPLETE", "Complete"; WARNING = "WARNING", "Warning"; DECOMMISSIONED = "DECOMMISSIONED", "Decommissioned";ERROR = "ERROR", "Error"
ValidationStatus.CHOICES=choices(ValidationStatus)

class SourceType(models.TextChoices):
    MANUAL = "MANUAL", "Manual"; IMPORT = "IMPORT", "Excel/CSV Import"; WIP_TRANSFER = "WIP_TRANSFER", "WIP Transfer"
SourceType.CHOICES=choices(SourceType)

class ApprovalStatus(models.TextChoices):
    NOT_SUBMITTED = "NOT_SUBMITTED", "Not Submitted"; PRINTED = "PRINTED", "Printed"; APPROVED = "APPROVED", "Approved"; REJECTED = "REJECTED", "Rejected";
ApprovalStatus.CHOICES=choices(ApprovalStatus)

class ActionType(models.TextChoices):
    CREATE = "CREATE", "Create"; EDIT = "EDIT", "Edit"; DELETE = "DELETE", "Delete"; IMPORT = "IMPORT", "Import"; ERROR_CORRECTION = "ERROR_CORRECTION", "Error Correction"; WIP_TRANSFER = "WIP_TRANSFER", "WIP Transfer"; PRINT = "PRINT", "Print"; VALIDATE = "VALIDATE", "Validate"; CAPITALIZE = "CAPITALIZE", "Capitalize"; BULK_CAPITALIZE = "BULK_CAPITALIZE", "Bulk Capitalize"
ActionType.CHOICES=choices(ActionType)

class ErrorType(models.TextChoices):
     WARNING = "WARNING", "Warning"; BLOCKING = "BLOCKING", "Blocking"
ErrorType.CHOICES=choices(ErrorType)

class DocumentType(models.TextChoices):
    INVOICE = "INVOICE", "Supplier Invoice"; PURCHASE_ORDER = "PURCHASE_ORDER", "Purchase Order"; DELIVERY_NOTE = "DELIVERY_NOTE", "Delivery Note"; APPROVAL = "APPROVAL", "Management Approval"; WIP_COMPLETION = "WIP_COMPLETION", "WIP Completion Report"; OTHER = "OTHER", "Other"
DocumentType.CHOICES=choices(DocumentType)

class StatusType(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"; VALIDATED = "VALIDATED", "Validated"; COMPLETED = "COMPLETED", "Completed"; FAILED = "FAILED", "Failed"
StatusType.CHOICES=choices(StatusType)