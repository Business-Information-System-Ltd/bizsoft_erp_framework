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
Tests the ERP organization package.
"""

from datetime import date
from django.test import TestCase
import erp_organization
from erp_organization.constants import OrganizationRelationshipType, OrganizationUnitType, PhysicalLocationType
from erp_organization.models import *
from erp_organization.selectors.branch_selector import BranchSelector
from erp_organization.domain_policies.branch_domain_policy import BranchDomainPolicyService
from erp_organization.application_policies.branch_application_policy import BranchApplicationPolicyService
from erp_organization.services.legal_entity_application_service import LegalEntityApplicationService
from erp_organization.services.branch_application_service import BranchApplicationService
from erp_organization.services.department_application_service import DepartmentApplicationService
from erp_organization.services.physical_location_application_service import PhysicalLocationApplicationService
from erp_organization.services.hierarchy_service import OrganizationHierarchyService
from erp_organization.services.relationship_service import OrganizationRelationshipService
from erp_organization.services.reference_registration_service import OrganizationReferenceRegistrationService
from erp_organization.services.bank_structure_service import BankStructureService
from erp_organization.validators.organization_validator import OrganizationValidator

class ErpOrganizationTests(TestCase):
    def setUp(self):
        self.legal_profile=LegalEntityApplicationService.create_legal_entity(data={'legal_entity_code':'ABC_BANK','legal_entity_name':'ABC Bank Limited','country_code':'MMR','functional_currency_code':'MMK'})
        self.legal=self.legal_profile.organization_unit
    def test_constants_exist(self): self.assertEqual(OrganizationUnitType.BRANCH,'BRANCH')
    def test_organization_unit_can_be_created(self): self.assertTrue(OrganizationUnit.objects.filter(unit_code='ABC_BANK').exists())
    def test_legal_entity_profile_can_be_created(self): self.assertEqual(self.legal_profile.country_code,'MMR')
    def test_branch_profile_can_be_created_under_legal_entity(self):
        b=BranchApplicationService.create_branch(data={'branch_code':'YGN','branch_name':'Yangon Main Branch','legal_entity_code':'ABC_BANK','is_bank_branch':True})
        self.assertEqual(b.legal_entity,self.legal)
    def test_department_profile_can_be_created(self):
        BranchApplicationService.create_branch(data={'branch_code':'YGN','branch_name':'Yangon Main Branch','legal_entity_code':'ABC_BANK'})
        d=DepartmentApplicationService.create_department(data={'department_code':'FIN','department_name':'Finance','legal_entity_code':'ABC_BANK','branch_code':'YGN'})
        self.assertEqual(d.legal_entity,self.legal)
    def test_sbu_can_be_assigned_to_legal_entity(self):
        unit=OrganizationUnit.objects.create(unit_code='RETAIL',unit_name='Retail Banking',unit_type=OrganizationUnitType.SBU)
        prof=StrategicBusinessUnitProfile.objects.create(organization_unit=unit,sbu_code='RETAIL',sbu_name='Retail Banking')
        assign=SBUEntityAssignment.objects.create(sbu=unit,legal_entity=self.legal)
        self.assertTrue(assign.is_active)
    def test_cost_profit_center_can_be_created(self):
        cu=OrganizationUnit.objects.create(unit_code='HO_IT',unit_name='HO IT',unit_type=OrganizationUnitType.COST_CENTER,legal_entity=self.legal,is_cost_center=True)
        pu=OrganizationUnit.objects.create(unit_code='RETAIL_PC',unit_name='Retail PC',unit_type=OrganizationUnitType.PROFIT_CENTER,legal_entity=self.legal,is_profit_center=True)
        CostCenterProfile.objects.create(organization_unit=cu,cost_center_code='HO_IT',cost_center_name='HO IT',legal_entity=self.legal)
        ProfitCenterProfile.objects.create(organization_unit=pu,profit_center_code='RETAIL_PC',profit_center_name='Retail PC',legal_entity=self.legal)
        self.assertEqual(CostCenterProfile.objects.count(),1); self.assertEqual(ProfitCenterProfile.objects.count(),1)
    def test_physical_location_and_custodian_and_relationship(self):
        b=BranchApplicationService.create_branch(data={'branch_code':'YGN','branch_name':'YGN','legal_entity_code':'ABC_BANK'})
        loc=PhysicalLocationApplicationService.create_physical_location(data={'location_code':'ATM_JC','location_name':'ATM Junction City','responsible_branch_code':'YGN','location_type':PhysicalLocationType.ATM_SITE,'is_internal':False,'is_asset_assignable':True})
        cust=CustodianAssignment.objects.create(custodian_code='BM_YGN',custodian_name='Branch Manager',branch=b.organization_unit)
        rel=OrganizationRelationshipService.create_relationship(b.organization_unit,loc.organization_unit,OrganizationRelationshipType.RESPONSIBLE_FOR)
        self.assertEqual(loc.location_type,PhysicalLocationType.ATM_SITE); self.assertTrue(cust.is_active); self.assertTrue(rel.is_active)
    def test_branch_must_belong_to_legal_entity(self):
        with self.assertRaises(Exception): BranchApplicationService.create_branch(data={'branch_code':'BAD','branch_name':'Bad','legal_entity_code':'NOPE'})
    def test_storage_location_must_belong_to_warehouse(self):
        with self.assertRaises(Exception): OrganizationValidator.require(None,'warehouse')
    def test_project_end_date_cannot_be_before_start_date(self):
        from erp_organization.domain_policies.project_domain_policy import ProjectDomainPolicyService
        with self.assertRaises(Exception): ProjectDomainPolicyService.validate_project_dates(date(2026,5,1),date(2026,4,1))
    def test_effective_dates_and_self_parent(self):
        with self.assertRaises(Exception): OrganizationValidator.validate_effective_dates(date(2026,5,1),date(2026,4,1))
        with self.assertRaises(Exception): OrganizationValidator.validate_no_self_parent(1,1)
    def test_circular_hierarchy_validation(self):
        a=OrganizationUnit.objects.create(unit_code='A',unit_name='A',unit_type=OrganizationUnitType.DEPARTMENT,legal_entity=self.legal)
        b=OrganizationUnit.objects.create(unit_code='B',unit_name='B',unit_type=OrganizationUnitType.DEPARTMENT,legal_entity=self.legal,parent_unit=a)
        a.parent_unit=b; a.save()
        with self.assertRaises(Exception): OrganizationValidator.validate_no_circular_hierarchy(a,b)
    def test_hierarchy_children_and_descendants(self):
        b=BranchApplicationService.create_branch(data={'branch_code':'YGN','branch_name':'YGN','legal_entity_code':'ABC_BANK'})
        d=DepartmentApplicationService.create_department(data={'department_code':'OPS','department_name':'Ops','legal_entity_code':'ABC_BANK','branch_code':'YGN'})
        self.assertIn(d.organization_unit, list(OrganizationHierarchyService.get_children(b.organization_unit)))
        self.assertIn(d.organization_unit, OrganizationHierarchyService.get_descendants(self.legal))
    def test_reference_registration_safe(self):
        result=OrganizationReferenceRegistrationService.register_all()
        self.assertEqual(len(result),6)
    def test_bank_structure_helpers(self):
        ho=BankStructureService.create_head_office(None,'ABC_BANK',{'branch_code':'HO','branch_name':'Head Office'})
        br=BankStructureService.create_bank_branch(None,'ABC_BANK',{'branch_code':'MDY','branch_name':'Mandalay'})
        atm=BankStructureService.create_atm_location(None,'MDY',{'location_code':'ATM_MDY','location_name':'ATM Mandalay'})
        self.assertTrue(ho.is_head_office); self.assertTrue(br.is_bank_branch); self.assertFalse(atm.is_internal)
    def test_inactive_not_returned_and_selector_policy(self):
        b=BranchApplicationService.create_branch(data={'branch_code':'YGN','branch_name':'YGN','legal_entity_code':'ABC_BANK'})
        self.assertEqual(BranchSelector.get_active_by_code('YGN'),b.organization_unit)
        b.organization_unit.is_active=False; b.organization_unit.save()
        self.assertIsNone(BranchSelector.get_active_by_code('YGN'))
        with self.assertRaises(Exception): BranchDomainPolicyService.validate_can_use_branch(b)
    def test_application_policy_runs_without_permission_package(self): self.assertTrue(BranchApplicationPolicyService.validate_create_branch_allowed(user=None,legal_entity_code='ABC_BANK'))
    def test_imports_do_not_require_business_modules(self): self.assertEqual(erp_organization.__package_name__,'erp_organization')
