"""
BizSoft ERP - Partners Module

File:
    erp_partners/services/partner_validation_service.py

Purpose:
    Provides partner usage validation for consuming ERP modules.

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


from django.utils import timezone

from erp_partners.enums.partner_enums import PartnerStatus
from erp_partners.models import Partner, PartnerRelationship, PartnerRole


class PartnerValidationService:
    @staticmethod
    def validate_partner_usage(partner_id, legal_entity_id, required_role=None, required_relationship=None, transaction_date=None):
        """Validate whether a partner can be used by another ERP module."""
        messages = []
        transaction_date = transaction_date or timezone.localdate()
        partner = Partner.objects.filter(id=partner_id).first()
        if not partner:
            return {'valid': False, 'messages': ['Partner does not exist.']}
        if not partner.is_active:
            messages.append('Partner is inactive.')
        if partner.status in {PartnerStatus.BLOCKED, PartnerStatus.BLACKLISTED}:
            messages.append(f'Partner status is {partner.status}.')
        if partner.status != PartnerStatus.ACTIVE:
            messages.append('Partner must be ACTIVE.')
        if required_role:
            if not PartnerRole.objects.filter(partner=partner, role_type=required_role, is_active=True, status=PartnerStatus.ACTIVE).exists():
                messages.append(f'Partner does not have active role {required_role}.')
        if required_relationship:
            qs = PartnerRelationship.objects.filter(
                from_partner=partner,
                legal_entity_id=legal_entity_id,
                relationship_type=required_relationship,
                is_active=True,
                status=PartnerStatus.ACTIVE,
            )
            qs = qs.filter(effective_from__isnull=True) | qs.filter(effective_from__lte=transaction_date)
            qs = qs.filter(effective_to__isnull=True) | qs.filter(effective_to__gte=transaction_date)
            if not qs.exists():
                messages.append(f'Partner does not have active relationship {required_relationship} for legal entity.')
        return {'valid': not messages, 'messages': messages}
