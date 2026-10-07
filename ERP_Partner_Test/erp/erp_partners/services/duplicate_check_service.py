from erp_partners.models import (
    Partner,
    PartnerContact
)


class DuplicateCheckService:

    @staticmethod
    def check_duplicate(data):

        results = []

        full_name = data.get("full_name")
        phone_no = data.get("phone_no")
        email = data.get("email")

        partners = (
            Partner.objects
            .filter(is_active=True)
        )

        for partner in partners:

            score = 0

            if (
                full_name
                and
                partner.display_name.lower()
                ==
                full_name.lower()
            ):
                score += 50

            if phone_no:

                phone_exists = (
                    PartnerContact.objects
                    .filter(
                        partner=partner,
                        contact_value=phone_no,
                        is_active=True
                    )
                    .exists()
                )

                if phone_exists:
                    score += 30

            if email:

                email_exists = (
                    PartnerContact.objects
                    .filter(
                        partner=partner,
                        contact_value=email,
                        is_active=True
                    )
                    .exists()
                )

                if email_exists:
                    score += 20

            if score > 0:

                results.append(
                    {
                        "partner_id":
                            str(partner.id),

                        "partner_code":
                            partner.partner_code,

                        "display_name":
                            partner.display_name,

                        "match_percentage":
                            score
                    }
                )

        return sorted(
            results,
            key=lambda x:
                x["match_percentage"],
            reverse=True
        )