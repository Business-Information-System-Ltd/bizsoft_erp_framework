"""
BizSoft ERP - Partners Module

File:
    erp_partners/serializers/validation_serializers.py

Purpose:
    Defines serializers for partner usage validation requests.

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


class PartnerUsageValidationSerializer(serializers.Serializer):
    partner_id = serializers.UUIDField()
    legal_entity_id = serializers.UUIDField(required=False, allow_null=True)
    required_role = serializers.CharField(required=False, allow_blank=True)
    required_relationship = serializers.CharField(required=False, allow_blank=True)
    transaction_date = serializers.DateField(required=False, allow_null=True)
