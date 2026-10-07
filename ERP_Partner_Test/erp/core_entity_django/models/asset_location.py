from django.db import models


class AssetLocationInfo(models.Model):

    asset = models.OneToOneField(
        "core_entity_django.AssetCore",
        on_delete=models.CASCADE,
        related_name="location_info",
    )

    legal_entity_id = models.BigIntegerField()

    branch_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    department_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    location_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    building_floor_room = models.CharField(
        max_length=255,
        blank=True,
    )

    rack_space_area = models.CharField(
        max_length=255,
        blank=True,
    )

    current_physical_status = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "far_asset_location_info"

        indexes = [
            models.Index(
                fields=["legal_entity_id"],
                name="idx_far_loc_legal_entity",
            ),
            models.Index(
                fields=["branch_id"],
                name="idx_far_loc_branch",
            ),
            models.Index(
                fields=["department_id"],
                name="idx_far_loc_department",
            ),
            models.Index(
                fields=["location_id"],
                name="idx_far_loc_location",
            ),
        ]