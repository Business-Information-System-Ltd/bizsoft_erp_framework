from erp_organization.models import (
    LegalEntityProfile,
    BranchProfile,
    DepartmentProfile,
    PhysicalLocationProfile,
)


class AssetReferenceSelector:

    @staticmethod
    def legal_entities():
        return LegalEntityProfile.objects.filter(
            is_active=True
        )

    @staticmethod
    def branches():
        return BranchProfile.objects.filter(
            is_active=True
        )

    @staticmethod
    def departments():
        return DepartmentProfile.objects.filter(
            is_active=True
        )

    @staticmethod
    def locations():
        return PhysicalLocationProfile.objects.filter(
            is_active=True
        )