# BizSoft ERP - Partners Module

Package: `erp_partners`  
First draft name requested by user. The original prompt name was `bizsoft_erp_partners`.

## Module Overview

`erp_partners` is the centralized ERP Business Partner / Stakeholder Master service. It manages natural persons and legal persons that can be used by Sales, Purchase, HR, FAR, Finance, Banking, Compliance, and other ERP modules.

The Partner module answers:

- Who is this person or organization?
- What role can this partner play?
- How is this partner formally related to a legal entity, organization unit, project, contract, asset, or business event?

Other modules answer what they do with the partner.

## Design Principles

- Partner is a centralized stakeholder master.
- Partner can be a natural person or legal person.
- One partner can have many roles.
- One partner can have many relationships.
- Formal relationships are anchored to `legal_entity_id` first.
- Partner stores common identity data only.
- Customer, Supplier, Employee, FAR, Finance, and Banking details belong to their own modules.

## Included Models

- `Partner`
- `PersonProfile`
- `LegalEntityProfile`
- `PartnerRole`
- `PartnerRelationship`
- `PartnerAddress`
- `PartnerContact`
- `PartnerIdentification`
- `PartnerRegistration`
- `PartnerComplianceSummary`

## Not Included

- Customer credit limit
- Supplier payment terms
- Employee payroll
- Fixed asset assignment history
- Bank reconciliation
- User permissions
- Authentication
- Accounting ledger balances

## Dependency Rule

Partner should remain independent. Sales, Purchase, HR, FAR, Finance, Banking, and Compliance depend on Partner. Partner must not depend on those modules.

## Legal Entity First Relationship Rule

Formal partner relationships should be anchored to `legal_entity_id` first. After that relationship exists, consuming modules may extend the partner relationship to organization units, projects, assets, contracts, and business events.

## Data Model Diagram

```text
Partner
  |-- PersonProfile
  |-- LegalEntityProfile
  |-- PartnerRole
  |-- PartnerRelationship
  |-- PartnerAddress
  |-- PartnerContact
  |-- PartnerIdentification
  |-- PartnerRegistration
  `-- PartnerComplianceSummary
```

## Example Usage

ABC Trading Co., Ltd. as Supplier:

```text
Partner: LEGAL_PERSON, display_name = ABC Trading
Role: SUPPLIER
Relationship: ABC Trading SUPPLIER_OF BizSoft Co., Ltd.
Purchase module later creates SupplierProfile.
```

U Aung Aung as Employee and Asset Custodian:

```text
Partner: NATURAL_PERSON, display_name = U Aung Aung
Roles: EMPLOYEE, ASSET_CUSTODIAN
HR later creates EmployeeProfile.
FAR later uses custodian_partner_id.
```

AYA Bank as Banker:

```text
Partner: LEGAL_PERSON, role = BANK
Relationship: AYA Bank BANKER_OF BizSoft Co., Ltd.
Banking module later creates Bank and BankAccount.
```

## API Examples

Create partner:

```json
{
  "partner_code": "ABC_TRADING",
  "partner_type": "LEGAL_PERSON",
  "display_name": "ABC Trading",
  "legal_name": "ABC Trading Co., Ltd.",
  "status": "DRAFT",
  "country_code": "MMR"
}
```

Add role:

```json
{
  "role_type": "SUPPLIER",
  "status": "ACTIVE",
  "is_primary_role": true
}
```

Add relationship:

```json
{
  "from_partner": "<supplier-partner-id>",
  "to_partner": "<company-partner-id>",
  "legal_entity_id": "<legal-entity-uuid>",
  "relationship_type": "SUPPLIER_OF",
  "relationship_category": "COMMERCIAL"
}
```

Validate partner usage:

```json
{
  "partner_id": "<partner-id>",
  "legal_entity_id": "<legal-entity-id>",
  "required_role": "SUPPLIER",
  "required_relationship": "SUPPLIER_OF",
  "transaction_date": "2026-06-04"
}
```

## API List

- `GET /api/partners/`
- `POST /api/partners/`
- `GET /api/partners/{id}/`
- `PUT/PATCH /api/partners/{id}/`
- `POST /api/partners/{id}/activate/`
- `POST /api/partners/{id}/block/`
- `GET/POST /api/partners/{id}/roles/`
- `GET/POST /api/partners/{id}/addresses/`
- `GET/POST /api/partners/{id}/contacts/`
- `GET/POST /api/partners/{id}/identifications/`
- `GET/POST /api/partners/{id}/registrations/`
- `GET/POST /api/partner-relationships/`
- `POST /api/partners/validate-usage/`

Filters:

```text
/api/partners/?partner_type=NATURAL_PERSON
/api/partners/?role_type=CUSTOMER
/api/partners/?status=ACTIVE
/api/partners/?search=ABC
```

## Validation Rules

- Partner code must be unique.
- Person profile only for `NATURAL_PERSON`.
- Legal entity profile only for `LEGAL_PERSON`, `GOVERNMENT_BODY`, or `INTERNAL_ORGANIZATION`.
- Effective end date must be greater than or equal to effective start date.
- Relationship partner cannot relate to itself.
- Relationship percentage must be between 0 and 100.
- Formal relationships require `legal_entity_id`.
- Email contacts must have valid email format.
- Only one primary address/contact/identification per partner and type.
- Identification/registration expiry date must be later than issue date.

## Future Extension Points

- `CustomerProfile` in Sales module
- `SupplierProfile` in Purchase module
- `EmployeeProfile` in HR module
- `PartnerBankAccount` in Banking module
- Detailed KYC/AML in Compliance module
- `UserAccount` link in Identity module

## Development Setup

```bash
pip install django djangorestframework
python manage.py makemigrations
python manage.py migrate
python manage.py test erp_partners
```

## Notes for Codex / Developers

Keep partner core clean. Do not add module-specific fields into Partner. Use service layer for business operations, repositories for data access, serializers for API validation, and `transaction.atomic` for create/update service operations.
