from django.db import models

from erp_partners.models.base import BaseModel


class PartnerRoleConflictRule(BaseModel):
    """
    Defines role conflict rule.

    Example

    EMPLOYEE
        +
    SUPPLIER

    => APPROVAL_REQUIRED
    """

    existing_role = models.CharField(
        max_length=100
    )

    new_role = models.CharField(
        max_length=100
    )

    result = models.CharField(
        max_length=100
    )

    message = models.TextField(
        blank=True
    )

    business_policy = models.ForeignKey(
        "erp_partners.BusinessPolicy",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="role_conflict_rules"
    )

    class Meta:
        db_table = "partner_role_conflict_rule"

        unique_together = (
            "existing_role",
            "new_role",
        )

    def __str__(self):

        return (
            f"{self.existing_role}"
            f" -> "
            f"{self.new_role}"
        )