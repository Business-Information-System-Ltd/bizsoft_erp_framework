"""
BizSoft ERP - Partners Module

File:
    erp_partners/apps.py

Purpose:
    Defines Django app configuration.

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

from django.apps import AppConfig


class ErpPartnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'erp_partners'
    verbose_name = 'ERP Partners'
