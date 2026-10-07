

from erp_partners.models import PartnerRole
from erp_partners.repositories.partner_role_conflict_repository import (
    PartnerRoleConflictRuleRepository,
)


class RoleConflictService:

    repository = PartnerRoleConflictRuleRepository()

    @classmethod
    def validate_role_change(cls, partner_id, new_role):

        existing_roles = PartnerRole.objects.filter(
            partner_id=partner_id,
            is_active=True
        )

        for role in existing_roles:
            
            rule = cls.repository.get_rule(
                existing_role=role.role_type,
                new_role=new_role
            )
            
            if rule:
                return {
                    "allowed": False,
                    "message": rule.message,
                    "result": rule.result,
                }

        return {
            "allowed": True,
            "message": "",
            "result": "ALLOW",
        }