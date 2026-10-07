# from erp_partners.repositories.business_policy_repository import (
#     BusinessPolicyRepository
# )

# class PolicyCheckService:

#     repository = BusinessPolicyRepository()

#     @classmethod
#     def get_policy(cls, policy_code):
#         return cls.repository.get_by_code(policy_code)

#     @classmethod
#     def policy_exists(cls, policy_code):
#         return cls.get_policy(policy_code) is not None

    
#     @classmethod
#     def validate_partner_action(
#         cls,
#         partner,
#         action,
#         role=None,
#         context=None
#     ):

       
#         result = {
#             "allowed": True,
#             "reason": None
#         }

#         if action == "ADD_ROLE" and role == "SUPPLIER":
#             if partner.partner_type == "NATURAL_PERSON":
#                 return {
#                     "allowed": False,
#                     "reason": "Natural Person cannot be SUPPLIER"
#                 }
            
#         if action == "ADD_ROLE" and role == "EMPLOYEE":
#             if partner.partner_type == "NATURAL_PERSON":
#                 return {
#                     "allowed": False,
#                     "reason": "Natural Person cannot be EMPLOYEE"
#                 }
            
#         if action == "ADD_ROLE" and role == "EMPLOYEE":
#             if partner.partner_type == "Legal_Person":
#                 return {
#                     "allowed": False,
#                     "reason": "Legal Person cannot be EMPLOYEE"
#                 }
        
#         if action == "ADD_ROLE" and role == "AUDITOR":
#             if partner.partner_type == "LEGAL_PERSON":
#                 return {
#                     "allowed": False,
#                     "reason": "LEGAL_PERSON cannot be AUDITOR"
#                 }

#         return result