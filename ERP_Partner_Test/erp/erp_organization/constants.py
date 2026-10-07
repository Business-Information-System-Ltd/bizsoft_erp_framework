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
Defines organization vocabulary and choices.
"""


def choices(cls):
    return [(v, k.replace('_', ' ').title()) for k, v in cls.__dict__.items() if k.isupper() and isinstance(v, str)]

class OrganizationUnitType:
    ENTERPRISE_GROUP='ENTERPRISE_GROUP'; LEGAL_ENTITY='LEGAL_ENTITY'; BRANCH='BRANCH'; DEPARTMENT='DEPARTMENT'; SBU='SBU'; FACILITY='FACILITY'; PLANT='PLANT'; STORE='STORE'; OFFICE='OFFICE'; WAREHOUSE='WAREHOUSE'; STORAGE_LOCATION='STORAGE_LOCATION'; PROCESS='PROCESS'; WORKSTATION='WORKSTATION'; PROJECT='PROJECT'; PROJECT_SITE='PROJECT_SITE'; COST_CENTER='COST_CENTER'; PROFIT_CENTER='PROFIT_CENTER'; PHYSICAL_LOCATION='PHYSICAL_LOCATION'; CUSTODIAN='CUSTODIAN'; OTHER='OTHER'
OrganizationUnitType.CHOICES=choices(OrganizationUnitType)

class OrganizationRelationshipType:
    BELONGS_TO='BELONGS_TO'; REPORTS_TO='REPORTS_TO'; OPERATES_UNDER='OPERATES_UNDER'; LOCATED_AT='LOCATED_AT'; ASSIGNED_TO='ASSIGNED_TO'; OWNS='OWNS'; SERVES='SERVES'; COST_ALLOCATED_TO='COST_ALLOCATED_TO'; PROFIT_REPORTED_TO='PROFIT_REPORTED_TO'; INVENTORY_STORED_AT='INVENTORY_STORED_AT'; ASSET_LOCATED_AT='ASSET_LOCATED_AT'; RESPONSIBLE_FOR='RESPONSIBLE_FOR'
OrganizationRelationshipType.CHOICES=choices(OrganizationRelationshipType)

class PhysicalLocationType:
    HEAD_OFFICE='HEAD_OFFICE'; BRANCH_OFFICE='BRANCH_OFFICE'; ATM_SITE='ATM_SITE'; VAULT='VAULT'; CASH_COUNTER='CASH_COUNTER'; DATA_CENTER='DATA_CENTER'; DR_SITE='DR_SITE'; SERVER_ROOM='SERVER_ROOM'; RECORD_ROOM='RECORD_ROOM'; CUSTOMER_SITE='CUSTOMER_SITE'; PUBLIC_SITE='PUBLIC_SITE'; VENDOR_SITE='VENDOR_SITE'; EMPLOYEE_SITE='EMPLOYEE_SITE'; OTHER='OTHER'
PhysicalLocationType.CHOICES=choices(PhysicalLocationType)

class UnitStatus:
    ACTIVE='ACTIVE'; INACTIVE='INACTIVE'; SUSPENDED='SUSPENDED'; CLOSED='CLOSED'
UnitStatus.CHOICES=choices(UnitStatus)

class CustodianType:
    EMPLOYEE='EMPLOYEE'; DEPARTMENT='DEPARTMENT'; BRANCH='BRANCH'; EXTERNAL='EXTERNAL'
CustodianType.CHOICES=choices(CustodianType)
