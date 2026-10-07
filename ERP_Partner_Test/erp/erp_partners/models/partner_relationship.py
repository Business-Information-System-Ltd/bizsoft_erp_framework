"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/partner_relationship.py

Purpose:
    Defines formal partner-to-partner relationships anchored to legal entity IDs.

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

from erp_partners.enums.partner_enums import PartnerStatus, RelationshipCategory, RelationshipType
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PartnerRelationship(BaseModel):
    from_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='relationships_from')
    to_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='relationships_to')
    legal_entity_id = models.UUIDField(null=True, blank=True, db_index=True)
    organization_unit_id = models.UUIDField(null=True, blank=True)
    relationship_type = models.CharField(max_length=60, choices=RelationshipType.choices)
    relationship_category = models.CharField(max_length=50, choices=RelationshipCategory.choices, default=RelationshipCategory.OTHER)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    number_of_shares = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    share_class = models.CharField(max_length=100, blank=True)
    contract_reference = models.CharField(max_length=150, blank=True)
    document_file_id = models.UUIDField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=PartnerStatus.choices, default=PartnerStatus.ACTIVE)

    class Meta:
        indexes = [models.Index(fields=['relationship_type']), models.Index(fields=['legal_entity_id']), models.Index(fields=['status'])]

    def __str__(self):
        return f'{self.from_partner} {self.relationship_type} {self.to_partner}'
