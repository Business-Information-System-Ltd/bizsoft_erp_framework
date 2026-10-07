"""
BizSoft ERP - Partners Module

File:
    erp_partners/repositories/partner_repository.py

Purpose:
    Provides persistence access for partners.

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


from erp_partners.models import Partner


class PartnerRepository:
    def get_by_id(self, partner_id):
        return Partner.objects.filter(id=partner_id).first()

    def get_by_code(self, partner_code):
        return Partner.objects.filter(partner_code=partner_code).first()

    def list_active(self):
        return Partner.objects.filter(is_active=True)

    def list_by_type(self, partner_type):
        return Partner.objects.filter(partner_type=partner_type, is_active=True)

    def list_by_role(self, role_type):
        return Partner.objects.filter(roles__role_type=role_type, roles__is_active=True, is_active=True).distinct()

    def exists_by_code(self, partner_code):
        return Partner.objects.filter(partner_code=partner_code).exists()

    def create(self, data):
        return Partner.objects.create(**data)

    def update(self, instance, data):
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
