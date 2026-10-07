from django.db import models


class AssetResponsibility(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="responsibility",
    )

    responsible_department_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    custodian_partner_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
    )

    asset_controller_partner_id = models.UUIDField(
        null=True,
        blank=True,
    )

    assigned_user_partner_id = models.UUIDField(
        null=True,
        blank=True,
    )