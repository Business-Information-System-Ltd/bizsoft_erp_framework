# from django.core.management.base import BaseCommand

# from erp_partners.models import PartnerRoleConflictRule


# class Command(BaseCommand):
#     help = "Seed Partner Role Conflict Rules"

#     def handle(self, *args, **kwargs):

#         rules = [
#             {
#                 "existing_role": "CUSTOMER",
#                 "new_role": "AUDITOR",
#                 "result": "BLOCK",
#                 "message": "Customer cannot also be Auditor.",
#             },
#             {
#                 "existing_role": "EMPLOYEE",
#                 "new_role": "SUPPLIER",
#                 "result": "APPROVAL_REQUIRED",
#                 "message": "Employee becoming Supplier requires approval.",
#             },
#             {
#                 "existing_role": "SUPPLIER",
#                 "new_role": "CUSTOMER",
#                 "result": "ALLOW",
#                 "message": "Supplier can also be Customer.",
#             },
#             {
#                 "existing_role": "AUDITOR",
#                 "new_role": "SUPPLIER",
#                 "result": "BLOCK",
#                 "message": "Auditor cannot also be Supplier.",
#             },
#             {
#                 "existing_role": "EMPLOYEE",
#                 "new_role": "CUSTOMER",
#                 "result": "ALLOW",
#                 "message": "Employee can also be Customer.",
#             },
#             {
#                 "existing_role": "LEGAL_PERSON",
#                 "new_role": "AUDITOR",
#                 "result": "BLOCK",
#                 "message": "Legal Person cannot also be Auditor.",
#             },
#         ]

#         for rule in rules:
#             PartnerRoleConflictRule.objects.get_or_create(
#                 existing_role=rule["existing_role"],
#                 new_role=rule["new_role"],
#                 defaults={
#                     "result": rule["result"],
#                     "message": rule["message"],
#                     "remarks": "Seed Data",
#                     "is_active": True,
#                 },
#             )

#         self.stdout.write(
#             self.style.SUCCESS(
#                 "Partner Role Conflict Rules seeded successfully."
#             )
#         )