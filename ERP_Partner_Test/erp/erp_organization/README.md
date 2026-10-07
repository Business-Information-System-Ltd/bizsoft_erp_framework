# BizSoft ERP - ERP Organization

Company: Business Information Systems Ltd. / BizSoft  
Author: Business Information Systems Ltd. / BizSoft  
Package: `erp_organization`  
Version: 1.0.0

`erp_organization` is the ERP business foundation package for enterprise operating structure. It defines legal ownership, operating responsibility, functional responsibility, strategic responsibility, accounting responsibility, physical location responsibility, and custodian responsibility.

Legal entity defines legal ownership. Branch defines operating responsibility. Department defines functional responsibility. SBU defines strategic business responsibility. Facility, warehouse, process, and workstation define operational structure. Project defines temporary business responsibility. Cost and profit centers define accounting responsibility. Physical location defines where assets or inventory actually exist. Custodian defines who is responsible.

Organization tells where and who. Dimension tells how to classify, summarize, analyze, and report.

## Purpose

The package supports simple companies, national banks, and future multinational structures. It avoids the limited `Company -> Branch -> Department` design and instead uses:

- `OrganizationUnit` as the common registry
- Profile tables for specific details
- Relationships for flexible hierarchy and many-to-many links
- Assignments for effective-dated responsibility
- Selectors for read/query access
- Domain policies for domain truth
- Application policies for use-case permission/context checks
- Application services for orchestration

## What Belongs Here

`erp_organization` owns master data and structure for:

- Enterprise groups
- Legal entities / companies
- Branches / head office / regional offices / zones
- Departments and functional hierarchy
- Strategic business units
- Facilities, plants, stores, offices, service centers
- Warehouses and storage locations
- Processes and workstations
- Projects and project sites
- Cost centers and profit centers
- Physical locations and fixed asset locations
- Custodian assignments
- Organization relationships and hierarchy

## What Does Not Belong Here

This package must not implement:

- Accounting posting
- Inventory stock movement
- Fixed asset depreciation
- Sales, purchase, payroll, or tax processing
- Workflow approval routing
- Permission engine
- Audit trail writing
- Notification sending
- Currency exchange calculation
- Project WBS detail costing

Other modules consume organization data. They decide how to use it.

## Architecture Pattern

Use this flow consistently:

```text
API / View / Controller
    -> Application Service
        -> Application Policy Service
            -> Domain Policy Service
                -> Selectors / Repositories / External Foundation Services
```

Selectors read data. Domain Policies validate domain truth. Application Policies validate whether an action is allowed in the current application context. Application Services orchestrate the use case.

## Key Models

### OrganizationUnit

Common registry for all organization-like units. Every legal entity, branch, department, SBU, warehouse, physical location, cost center, and profit center has an `OrganizationUnit` record.

Important fields:

- `unit_code`
- `unit_name`
- `unit_type`
- `legal_entity`
- `parent_unit`
- `is_cost_center`
- `is_profit_center`
- `is_inventory_storable`
- `is_asset_assignable`
- `is_active`
- `effective_from`
- `effective_to`

### Profile Tables

Profile tables hold specific fields for each unit type. Examples:

- `LegalEntityProfile`: country, functional currency, legal name, registration number
- `BranchProfile`: legal entity, region, zone, head office flag, bank branch flag
- `DepartmentProfile`: legal entity, branch, parent department
- `CostCenterProfile`: legal entity, branch, department responsibility
- `ProfitCenterProfile`: legal entity and reporting responsibility
- `PhysicalLocationProfile`: ATM, vault, server room, data center, public site, etc.
- `WarehouseProfile` and `StorageLocationProfile`: inventory structure
- `ProjectProfile` and `ProjectSiteProfile`: temporary responsibility structure
- `CustodianAssignment`: who is responsible for assets or locations

### OrganizationRelationship

Flexible relationship table for cases where simple parent-child hierarchy is not enough.

Examples:

- Branch belongs to legal entity
- ATM is responsible under a branch
- Department reports to another department
- Warehouse is located at a facility
- Cost center is allocated to a department
- Asset location is assigned to a branch

## Constants

Important constants are in [constants.py](C:/erp_project/erp_organization/constants.py):

- `OrganizationUnitType`
- `OrganizationRelationshipType`
- `PhysicalLocationType`
- `UnitStatus`
- `CustodianType`

Banking physical location examples:

- `HEAD_OFFICE`
- `BRANCH_OFFICE`
- `ATM_SITE`
- `VAULT`
- `CASH_COUNTER`
- `DATA_CENTER`
- `DR_SITE`
- `SERVER_ROOM`
- `RECORD_ROOM`
- `CUSTOMER_SITE`
- `PUBLIC_SITE`
- `VENDOR_SITE`
- `EMPLOYEE_SITE`

## Small Organization Example

A small company can keep setup simple:

- Legal Entity: ABC Co., Ltd.
- Branch: Head Office
- Departments: Finance, Sales, Admin
- Cost Centers: Finance HO, Sales HO
- Physical Locations: Office Building, Room 101

Only the necessary structures need to be created.

## National Bank Example

A national bank can use richer structure:

- Legal Entity: ABC Bank Limited
- Head Office: HO
- Branches: YGN Main, MDY Branch, NPT Branch
- Departments: Credit, Treasury, Operations, IT, Risk, Compliance, Internal Audit
- Cost Centers: HO IT, HO Finance, YGN Operations
- Profit Centers: Retail Banking, Corporate Banking, Digital Banking
- Physical Locations: ATM Junction City, Data Center 10th Mile, DR Site Mandalay, Vault YGN Branch
- Custodians: Branch Manager, IT Department, Cash Department

## Fixed Asset Assignment Example

An ATM can be physically outside the branch but administratively assigned to a branch and department.

Example structure:

- Legal Entity: ABC Bank
- Responsible Branch: YGN Main Branch
- Department: Digital Banking
- Cost Center: Digital Banking Cost Center
- Physical Location: `ATM_SITE` - Junction City Mall
- Custodian: IT Department or assigned officer

FAR should use this package for responsibility and location. FAR should still own depreciation, capitalization, transfer, disposal, and asset transaction logic.

## Inventory Location Example

Inventory can use:

- Legal Entity
- Facility
- Warehouse
- Storage Location
- Bin or rack later if needed

`erp_organization` defines where inventory can be stored. Inventory module owns stock movement and valuation.

## Example: Create Legal Entity

```python
from erp_organization.services.legal_entity_application_service import LegalEntityApplicationService

legal = LegalEntityApplicationService.create_legal_entity(
    data={
        "legal_entity_code": "ABC_BANK",
        "legal_entity_name": "ABC Bank Limited",
        "country_code": "MMR",
        "functional_currency_code": "MMK",
    }
)
```

## Example: Create Branch

```python
from erp_organization.services.branch_application_service import BranchApplicationService

branch = BranchApplicationService.create_branch(
    data={
        "branch_code": "YGN",
        "branch_name": "Yangon Main Branch",
        "legal_entity_code": "ABC_BANK",
        "region_code": "YGN_REGION",
        "zone_code": "LOWER_MYANMAR",
        "is_bank_branch": True,
        "is_head_office": False,
    }
)
```

## Example: Create Department

```python
from erp_organization.services.department_application_service import DepartmentApplicationService

department = DepartmentApplicationService.create_department(
    data={
        "department_code": "FIN",
        "department_name": "Finance Department",
        "legal_entity_code": "ABC_BANK",
        "branch_code": "YGN",
    }
)
```

## Example: Create ATM Location

```python
from erp_organization.constants import PhysicalLocationType
from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService

location = PhysicalLocationApplicationService.create_physical_location(
    data={
        "location_code": "ATM_JC",
        "location_name": "ATM Junction City",
        "responsible_branch_code": "YGN",
        "location_type": PhysicalLocationType.ATM_SITE,
        "is_internal": False,
        "is_asset_assignable": True,
    }
)
```

## Example: Bank Helper Service

```python
from erp_organization.services.bank_structure_service import BankStructureService

head_office = BankStructureService.create_head_office(
    user=None,
    legal_entity_code="ABC_BANK",
    branch_data={
        "branch_code": "HO",
        "branch_name": "Head Office",
    },
)

atm = BankStructureService.create_atm_location(
    user=None,
    branch_code="HO",
    location_data={
        "location_code": "ATM_HO_001",
        "location_name": "Head Office ATM 001",
    },
)
```

## Selector Usage

Selectors are read/query side helpers. They do not write.

```python
from erp_organization.selectors.branch_selector import BranchSelector

branch_unit = BranchSelector.get_active_by_code("YGN")
branches = BranchSelector.list_active()
```

## Domain Policy Usage

Domain policies validate business truth that should always be true regardless of UI, API, import, or background job.

```python
from erp_organization.domain_policies.branch_domain_policy import BranchDomainPolicyService

BranchDomainPolicyService.validate_can_use_branch(branch_unit)
```

## Application Policy Usage

Application policies validate use-case context. Later they can call `erp_permission`, `erp_configuration`, or module activation services.

```python
from erp_organization.application_policies.branch_application_policy import BranchApplicationPolicyService

BranchApplicationPolicyService.validate_create_branch_allowed(
    user=request.user,
    legal_entity_code="ABC_BANK",
)
```

## Hierarchy Usage

```python
from erp_organization import OrganizationHierarchyService

children = OrganizationHierarchyService.get_children(branch_unit)
descendants = OrganizationHierarchyService.get_descendants(legal_entity_unit)
tree = OrganizationHierarchyService.get_tree()
```

## Relationship Usage

```python
from erp_organization.constants import OrganizationRelationshipType
from erp_organization.services.relationship_service import OrganizationRelationshipService

relationship = OrganizationRelationshipService.create_relationship(
    from_unit=branch_unit,
    to_unit=location_unit,
    relationship_type=OrganizationRelationshipType.RESPONSIBLE_FOR,
)
```

## Reference Lookup Registration

```python
from erp_organization import OrganizationReferenceRegistrationService

OrganizationReferenceRegistrationService.register_all()
```

This prepares reference lookup metadata for:

- `LEGAL_ENTITY`
- `BRANCH`
- `DEPARTMENT`
- `COST_CENTER`
- `PROFIT_CENTER`
- `PHYSICAL_LOCATION`

The registration is safe if `core_db` is unavailable.

## API Endpoints

Base path:

```text
/api/erp-organization/
```

Available endpoints:

- `/api/erp-organization/organization/units/`
- `/api/erp-organization/organization/legal-entities/`
- `/api/erp-organization/organization/branches/`
- `/api/erp-organization/organization/departments/`
- `/api/erp-organization/organization/cost-centers/`
- `/api/erp-organization/organization/profit-centers/`
- `/api/erp-organization/organization/locations/`
- `/api/erp-organization/organization/tree/`
- `/api/erp-organization/organization/bank/branches/`
- `/api/erp-organization/organization/bank/atm-locations/`

The first version keeps API views simple. Final permission control should be integrated later with `erp_permission`.

## Validation Rules

Important validation rules:

- Legal entity must have country and functional currency.
- Branch must belong to legal entity.
- Warehouse must belong to legal entity and optionally branch/facility/project site.
- Storage location must belong to warehouse.
- Department can be hierarchical, but hierarchy must not create circular reference.
- SBU may be assigned to multiple legal entities.
- Project must have start date.
- Project end date must not be before start date.
- Cost center must belong to legal entity.
- Profit center must belong to legal entity.
- Physical asset location should have responsible branch or department if asset assignable.
- A unit cannot be parent of itself.
- Inactive units cannot be used in new transactions.
- `effective_from` must be before or equal to `effective_to`.
- Codes should use uppercase letters, numbers, underscore, or hyphen. Avoid spaces.
- National bank branch must belong to the bank legal entity.
- ATM physical location may be external/public but should have responsible branch.

## Relationship With Other Packages

### erp_configuration

Controls whether multi-company, multi-branch, multi-department, multi-cost-center, multi-project, and multi-location are enabled.

### erp_dimension

Can use organization data as value sources for dimensions such as branch, department, cost center, profit center, project, SBU, and location.

### GL

Uses legal entity, branch, department, cost center, profit center, project, and SBU as accounting and reporting dimensions.

### FAR

Uses legal entity, branch, department, cost center, profit center, physical location, project, and custodian for asset assignment and depreciation cost allocation.

### Inventory

Uses legal entity, facility, warehouse, storage location, process, workstation, and project site for stock tracking.

### Workflow / Approval

Uses organization structure for routing context. Approval routing logic belongs to workflow/approval packages, not here.

### Project Costing

Uses project and project site from `erp_organization`. Detailed WBS belongs to project costing.

## Common Data Entry Order

Recommended first setup order:

1. Create legal entity.
2. Create head office branch.
3. Create branches.
4. Create departments.
5. Create cost centers and profit centers.
6. Create physical locations.
7. Create custodians.
8. Create optional SBU, facility, warehouse, storage location, and project structures.
9. Register reference lookups.

## Developer Notes

Use selectors for reads:

```python
BranchSelector.get_active_by_code("YGN")
```

Use application services for writes:

```python
BranchApplicationService.create_branch(data={...})
```

Do not write business rules directly inside views. Views should receive request, call service, return response.

Do not use repositories directly from API views unless the use case is intentionally very small. Repositories are persistence helpers, not business orchestration.

## Future Extension Notes

Future extensions may include:

- Advanced WBS in project costing
- Manufacturing routing in manufacturing module
- Inventory valuation and stock movement in inventory module
- Fixed asset depreciation and movement in FAR module
- Approval routing in workflow/approval modules
- Permission checks in `erp_permission`
- Business audit trail in `erp_audit`
- Optimized tree queries using `core_db`
- Dimension rules using `erp_dimension`
- HR employee master integration
- Geographic master data in localization/master data package
- Multi-country tax/legal compliance in tax/legal modules

## Customization and Industry-Specific Organization Types

`erp_organization` is designed to be flexible, but it should remain generic. It should provide common organization structure that many ERP modules can use. It should not become a place where every customer-specific or industry-specific rule is hard-coded.

The correct arrangement is:

```text
erp_organization
    Generic ERP organization foundation
    Legal entity, branch, department, SBU, facility, warehouse, project,
    cost center, profit center, physical location, custodian, relationship

bizsoft.erp.bank.* or erp_bank
    Banking-specific organization helpers
    Bank branch setup, ATM setup, vault setup, data center setup,
    DR site setup, banking default structures, banking validation helpers

bizsoft.erp.customer_x.* or customer_x_customization
    Customer-specific organization extensions
    Customer-specific naming, approval, import, default setup,
    mapping, and special validation
```

### Is the Existing Design Flexible?

Yes. The existing design is flexible because it uses:

- `OrganizationUnit` as a common registry
- `unit_type` to identify the kind of organization unit
- Profile tables for special details
- `OrganizationRelationship` for flexible hierarchy and many-to-many links
- Effective dates for assignments and relationships
- Boolean capability flags such as `is_asset_assignable`, `is_inventory_storable`, `is_cost_center`, and `is_profit_center`
- Services and policies that can be extended without changing the core models

This means the same foundation can support a small company, a bank, a manufacturing company, a retailer, or a multinational group.

### What Should Stay in erp_organization

Keep generic ERP organization concepts here:

- Legal entity
- Branch
- Department
- SBU
- Facility
- Warehouse
- Storage location
- Project
- Project site
- Cost center
- Profit center
- Physical location
- Custodian
- Organization hierarchy
- Organization relationship
- Effective-dated assignment
- Reference lookup support

Generic examples:

```python
BranchApplicationService.create_branch(...)
PhysicalLocationApplicationService.create_physical_location(...)
OrganizationRelationshipService.create_relationship(...)
```

These are safe to keep in `erp_organization` because they are useful for many industries.

### What Should Move to Industry or Customer Packages

Move industry-specific helpers out of `erp_organization` when the service name or rule belongs to one industry.

Banking-specific examples:

```python
BankStructureService.create_bank_branch(...)
BankStructureService.create_atm_location(...)
BankStructureService.create_vault_location(...)
BankStructureService.create_dr_site(...)
```

These should live in a banking extension package, for example:

```text
bizsoft/erp/bank/organization/services/bank_structure_service.py
```

or:

```text
erp_bank/
    organization/
        services/
            bank_structure_service.py
```

Customer-specific examples:

```python
CustomerXOrganizationSetupService.create_default_regions(...)
CustomerXBranchImportService.import_legacy_branch_file(...)
CustomerXApprovalOrgMappingService.map_department_to_approver(...)
```

These should live in a customer customization package, not in `erp_organization`.

### Arrangement Rules

Use these rules when deciding where code belongs:

| Question | Put in erp_organization | Put in industry/customer package |
| --- | --- | --- |
| Is it useful for most ERP customers? | Yes | No |
| Is it a generic legal/branch/department/location concept? | Yes | No |
| Does it mention bank, hospital, school, hotel, manufacturing, or a customer name? | No | Yes |
| Does it implement customer-specific import, naming, or approval setup? | No | Yes |
| Does it only create a generic physical location? | Yes | No |
| Does it create an ATM, vault, teller counter, ward, classroom, production line, or hotel room? | Maybe as `location_type`, but service should be outside | Yes |

### Recommended Extension Structure

For banking:

```text
bizsoft/
    erp/
        bank/
            __init__.py
            organization/
                __init__.py
                services/
                    bank_structure_service.py
                policies/
                    bank_branch_policy.py
                selectors/
                    bank_branch_selector.py
                README.md
```

For a customer-specific package:

```text
bizsoft/
    customers/
        abc_bank/
            __init__.py
            organization/
                services/
                    abc_bank_setup_service.py
                    abc_bank_branch_import_service.py
                policies/
                    abc_bank_organization_policy.py
                mappings/
                    legacy_branch_mapping.py
                README.md
```

### Example: Generic Physical Location vs Bank ATM

Generic foundation service:

```python
from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService
from erp_organization.constants import PhysicalLocationType

location = PhysicalLocationApplicationService.create_physical_location(
    data={
        "location_code": "ATM_JC",
        "location_name": "ATM Junction City",
        "location_type": PhysicalLocationType.ATM_SITE,
        "responsible_branch_code": "YGN",
        "is_internal": False,
        "is_asset_assignable": True,
    }
)
```

Banking extension helper:

```python
from bizsoft.erp.bank.organization.services.bank_structure_service import BankStructureService

location = BankStructureService.create_atm_location(
    user=request.user,
    branch_code="YGN",
    location_data={
        "location_code": "ATM_JC",
        "location_name": "ATM Junction City",
    },
)
```

The banking helper can call the generic `PhysicalLocationApplicationService` internally. This keeps generic ERP foundation clean while still giving banking users an easy API.

### Profile Table Extension Rule

If a new organization type only needs normal fields, use `OrganizationUnit` plus existing profile tables.

If it needs special fields that are not useful for most ERP customers, create a separate detail/profile table in the extension package.

Example banking extension detail table:

```python
class BankBranchDetail(models.Model):
    branch = models.OneToOneField(
        "erp_organization.BranchProfile",
        on_delete=models.CASCADE,
        related_name="bank_detail",
    )
    central_bank_branch_code = models.CharField(max_length=50, blank=True)
    clearing_branch_code = models.CharField(max_length=50, blank=True)
    cash_limit_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    is_clearing_branch = models.BooleanField(default=False)
```

Do not add these fields directly to `BranchProfile` unless they are truly generic for all ERP customers.

### Customization Rule Summary

Use `erp_organization` for the foundation. Use industry packages for industry convenience services. Use customer packages for customer-specific rules.

This keeps the ERP foundation reusable, understandable, and stable while still allowing deep customization.
