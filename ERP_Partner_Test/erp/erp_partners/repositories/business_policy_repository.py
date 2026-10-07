from erp_partners.models.business_policy import (
    BusinessPolicy
)


class BusinessPolicyRepository:

    @staticmethod
    def get_all():

        return (
            BusinessPolicy.objects
            .filter(is_active=True)
            .order_by("policy_code")
        )

    @staticmethod
    def get_by_id(policy_id):

        return (
            BusinessPolicy.objects
            .filter(
                id=policy_id,
                is_active=True
            )
            .first()
        )

    @staticmethod
    def get_by_code(policy_code):

        return (
            BusinessPolicy.objects
            .filter(
                policy_code=policy_code,
                is_active=True
            )
            .first()
        )

    @staticmethod
    def create(**kwargs):

        return (
            BusinessPolicy.objects
            .create(**kwargs)
        )
    @staticmethod
    def list_active():
        return BusinessPolicy.objects.filter(
            is_active=True
        )

    @staticmethod
    def save(policy):

        policy.save()

        return policy