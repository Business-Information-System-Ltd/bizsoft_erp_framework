from erp_partners.models.legal_entity_profile import LegalEntityProfile


class LegalEntityService:

    @staticmethod
    def create_legal_entity(data):
        return LegalEntityProfile.objects.create(**data)

    @staticmethod
    def get_legal_entity(entity_id):
        return LegalEntityProfile.objects.get(id=entity_id)