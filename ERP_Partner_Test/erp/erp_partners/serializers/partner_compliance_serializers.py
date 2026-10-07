"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/partner_compliance_serializers.py

Purpose:
    Defines serializers for partner compliance summary.

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


from rest_framework import serializers

from erp_partners.models import PartnerComplianceSummary


class PartnerComplianceSummarySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PartnerComplianceSummary
        fields = '__all__'
