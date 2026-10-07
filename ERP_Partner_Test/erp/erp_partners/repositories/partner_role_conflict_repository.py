from erp_partners.models.partner_role_conflict_rule import PartnerRoleConflictRule


class PartnerRoleConflictRuleRepository:

    def get_rule(
        self,
        existing_role,
        new_role,
    ):
        return (
            PartnerRoleConflictRule.objects
            .filter(
                existing_role=existing_role,
                new_role=new_role,
                is_active=True,
            )
            .select_related("business_policy")
            .first()
        )

    def list_by_existing_role(
        self,
        existing_role,
    ):
        return (
            PartnerRoleConflictRule.objects
            .filter(
                existing_role=existing_role,
                is_active=True,
            )
        )