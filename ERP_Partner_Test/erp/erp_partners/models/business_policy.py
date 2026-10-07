from django.db import models

from erp_partners.models.base import BaseModel


class BusinessPolicy(BaseModel):
    """
    Business policy master.

    Stores configurable backend policy used during
    partner onboarding and role validation.
    """

    policy_code = models.CharField(
        max_length=100,
        unique=True
    )

    policy_name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = "partner_business_policy"
        ordering = [
            "policy_code"
        ]

    def __str__(self):
        return self.policy_name