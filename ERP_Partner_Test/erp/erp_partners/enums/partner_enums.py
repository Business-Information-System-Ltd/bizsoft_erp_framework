"""
BizSoft ERP - Partners Module

File:
    erp_partners/enums/partner_enums.py

Purpose:
    Defines partner enums and Django TextChoices.

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


from django.db import models


class PartnerType(models.TextChoices):
    NATURAL_PERSON = 'NATURAL_PERSON', 'Natural Person'
    LEGAL_PERSON = 'LEGAL_PERSON', 'Legal Person'
    GOVERNMENT_BODY = 'GOVERNMENT_BODY', 'Government Body'
    INTERNAL_ORGANIZATION = 'INTERNAL_ORGANIZATION', 'Internal Organization'
    OTHER = 'OTHER', 'Other'


class PartnerStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    BLOCKED = 'BLOCKED', 'Blocked'
    BLACKLISTED = 'BLACKLISTED', 'Blacklisted'


class PersonGender(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'
    NOT_SPECIFIED = 'NOT_SPECIFIED', 'Not Specified'


class PartnerRoleType(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    SUPPLIER = 'SUPPLIER', 'Supplier'
    EMPLOYEE = 'EMPLOYEE', 'Employee'
    DIRECTOR = 'DIRECTOR', 'Director'
    SHAREHOLDER = 'SHAREHOLDER', 'Shareholder'
    BENEFICIAL_OWNER = 'BENEFICIAL_OWNER', 'Beneficial Owner'
    BANK = 'BANK', 'Bank'
    AUDITOR = 'AUDITOR', 'Auditor'
    CONSULTANT = 'CONSULTANT', 'Consultant'
    LEGAL_ADVISOR = 'LEGAL_ADVISOR', 'Legal Advisor'
    TAX_ADVISOR = 'TAX_ADVISOR', 'Tax Advisor'
    REGULATOR = 'REGULATOR', 'Regulator'
    AGENT = 'AGENT', 'Agent'
    CONTRACTOR = 'CONTRACTOR', 'Contractor'
    SUBCONTRACTOR = 'SUBCONTRACTOR', 'Subcontractor'
    LANDLORD = 'LANDLORD', 'Landlord'
    TENANT = 'TENANT', 'Tenant'
    ASSET_CUSTODIAN = 'ASSET_CUSTODIAN', 'Asset Custodian'
    CONTACT_PERSON = 'CONTACT_PERSON', 'Contact Person'
    GUARANTOR = 'GUARANTOR', 'Guarantor'
    AUTHORIZED_SIGNATORY = 'AUTHORIZED_SIGNATORY', 'Authorized Signatory'
    SERVICE_PROVIDER = 'SERVICE_PROVIDER', 'Service Provider'
    OTHER = 'OTHER', 'Other'


class RelationshipType(models.TextChoices):
    CUSTOMER_OF = 'CUSTOMER_OF', 'Customer Of'
    SUPPLIER_OF = 'SUPPLIER_OF', 'Supplier Of'
    EMPLOYEE_OF = 'EMPLOYEE_OF', 'Employee Of'
    DIRECTOR_OF = 'DIRECTOR_OF', 'Director Of'
    SHAREHOLDER_OF = 'SHAREHOLDER_OF', 'Shareholder Of'
    BENEFICIAL_OWNER_OF = 'BENEFICIAL_OWNER_OF', 'Beneficial Owner Of'
    CONTACT_PERSON_OF = 'CONTACT_PERSON_OF', 'Contact Person Of'
    AUTHORIZED_SIGNATORY_OF = 'AUTHORIZED_SIGNATORY_OF', 'Authorized Signatory Of'
    GUARANTOR_OF = 'GUARANTOR_OF', 'Guarantor Of'
    BANKER_OF = 'BANKER_OF', 'Banker Of'
    LENDER_TO = 'LENDER_TO', 'Lender To'
    BORROWER_FROM = 'BORROWER_FROM', 'Borrower From'
    AUDITOR_OF = 'AUDITOR_OF', 'Auditor Of'
    CONSULTANT_OF = 'CONSULTANT_OF', 'Consultant Of'
    LEGAL_ADVISOR_OF = 'LEGAL_ADVISOR_OF', 'Legal Advisor Of'
    TAX_ADVISOR_OF = 'TAX_ADVISOR_OF', 'Tax Advisor Of'
    REGULATOR_OF = 'REGULATOR_OF', 'Regulator Of'
    SERVICE_PROVIDER_OF = 'SERVICE_PROVIDER_OF', 'Service Provider Of'
    CONTRACTOR_OF = 'CONTRACTOR_OF', 'Contractor Of'
    SUBCONTRACTOR_OF = 'SUBCONTRACTOR_OF', 'Subcontractor Of'
    LANDLORD_OF = 'LANDLORD_OF', 'Landlord Of'
    TENANT_OF = 'TENANT_OF', 'Tenant Of'
    RELATED_PARTY_OF = 'RELATED_PARTY_OF', 'Related Party Of'
    FAMILY_MEMBER_OF = 'FAMILY_MEMBER_OF', 'Family Member Of'
    CUSTODIAN_OF = 'CUSTODIAN_OF', 'Custodian Of'
    RESPONSIBLE_PERSON_OF = 'RESPONSIBLE_PERSON_OF', 'Responsible Person Of'
    APPROVER_FOR = 'APPROVER_FOR', 'Approver For'
    REQUESTER_FOR = 'REQUESTER_FOR', 'Requester For'
    OTHER = 'OTHER', 'Other'


class RelationshipCategory(models.TextChoices):
    COMMERCIAL = 'COMMERCIAL', 'Commercial'
    EMPLOYMENT = 'EMPLOYMENT', 'Employment'
    GOVERNANCE = 'GOVERNANCE', 'Governance'
    OWNERSHIP = 'OWNERSHIP', 'Ownership'
    PROFESSIONAL_SERVICE = 'PROFESSIONAL_SERVICE', 'Professional Service'
    BANKING_FINANCE = 'BANKING_FINANCE', 'Banking Finance'
    REGULATORY = 'REGULATORY', 'Regulatory'
    OPERATIONAL = 'OPERATIONAL', 'Operational'
    FAMILY = 'FAMILY', 'Family'
    RELATED_PARTY = 'RELATED_PARTY', 'Related Party'
    OTHER = 'OTHER', 'Other'


class AddressType(models.TextChoices):
    REGISTERED = 'REGISTERED', 'Registered'
    BUSINESS = 'BUSINESS', 'Business'
    BILLING = 'BILLING', 'Billing'
    SHIPPING = 'SHIPPING', 'Shipping'
    RESIDENTIAL = 'RESIDENTIAL', 'Residential'
    PERMANENT = 'PERMANENT', 'Permanent'
    MAILING = 'MAILING', 'Mailing'
    OFFICE = 'OFFICE', 'Office'
    FACTORY = 'FACTORY', 'Factory'
    WAREHOUSE = 'WAREHOUSE', 'Warehouse'
    BRANCH = 'BRANCH', 'Branch'
    OTHER = 'OTHER', 'Other'


class ContactType(models.TextChoices):
    MOBILE = 'MOBILE', 'Mobile'
    PHONE = 'PHONE', 'Phone'
    EMAIL = 'EMAIL', 'Email'
    WEBSITE = 'WEBSITE', 'Website'
    VIBER = 'VIBER', 'Viber'
    WHATSAPP = 'WHATSAPP', 'WhatsApp'
    TELEGRAM = 'TELEGRAM', 'Telegram'
    FAX = 'FAX', 'Fax'
    HOTLINE = 'HOTLINE', 'Hotline'
    OTHER = 'OTHER', 'Other'


class IdentificationType(models.TextChoices):
    NRC = 'NRC', 'NRC'
    PASSPORT = 'PASSPORT', 'Passport'
    DRIVER_LICENSE = 'DRIVER_LICENSE', 'Driver License'
    TAX_ID = 'TAX_ID', 'Tax ID'
    SOCIAL_SECURITY_NO = 'SOCIAL_SECURITY_NO', 'Social Security No'
    EMPLOYEE_ID = 'EMPLOYEE_ID', 'Employee ID'
    STUDENT_ID = 'STUDENT_ID', 'Student ID'
    OTHER = 'OTHER', 'Other'


class RegistrationType(models.TextChoices):
    COMPANY_REGISTRATION = 'COMPANY_REGISTRATION', 'Company Registration'
    BUSINESS_LICENSE = 'BUSINESS_LICENSE', 'Business License'
    DICA_REGISTRATION = 'DICA_REGISTRATION', 'DICA Registration'
    TAX_REGISTRATION = 'TAX_REGISTRATION', 'Tax Registration'
    COMMERCIAL_TAX_REGISTRATION = 'COMMERCIAL_TAX_REGISTRATION', 'Commercial Tax Registration'
    IMPORT_EXPORT_LICENSE = 'IMPORT_EXPORT_LICENSE', 'Import Export License'
    FINANCIAL_INSTITUTION_LICENSE = 'FINANCIAL_INSTITUTION_LICENSE', 'Financial Institution License'
    NGO_REGISTRATION = 'NGO_REGISTRATION', 'NGO Registration'
    PROFESSIONAL_LICENSE = 'PROFESSIONAL_LICENSE', 'Professional License'
    OTHER = 'OTHER', 'Other'


class KYCStatus(models.TextChoices):
    NOT_REQUIRED = 'NOT_REQUIRED', 'Not Required'
    PENDING = 'PENDING', 'Pending'
    VERIFIED = 'VERIFIED', 'Verified'
    REJECTED = 'REJECTED', 'Rejected'
    EXPIRED = 'EXPIRED', 'Expired'


class RiskLevel(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'
    NOT_ASSESSED = 'NOT_ASSESSED', 'Not Assessed'


class ScreeningStatus(models.TextChoices):
    NOT_SCREENED = 'NOT_SCREENED', 'Not Screened'
    CLEAR = 'CLEAR', 'Clear'
    POSSIBLE_MATCH = 'POSSIBLE_MATCH', 'Possible Match'
    CONFIRMED_MATCH = 'CONFIRMED_MATCH', 'Confirmed Match'
    REJECTED = 'REJECTED', 'Rejected'
