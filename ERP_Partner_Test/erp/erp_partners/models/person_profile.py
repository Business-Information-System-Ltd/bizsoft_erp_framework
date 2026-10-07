"""
BizSoft ERP - Partners Module

File:
    erp_partners/models/person_profile.py

Purpose:
    Defines natural person profile data for a partner.

Architectural Notes:
    - This module manages common Business Partner / Stakeholder master data.
    - Customer, Supplier, Employee, FAR, Finance, and other module-specific profiles
      must be implemented in their respective modules.
    - This module should remain a core shared service with minimum external dependency.

Author:
    BizSoft Systems

Created:
    2026-06-04
"""


from django.db import models

from erp_partners.enums.partner_enums import PersonGender
from erp_partners.models.base import BaseModel
from erp_partners.models.partner import Partner


class PersonProfile(BaseModel):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='person_profile')
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=255)
    name_in_myanmar = models.CharField(max_length=255, blank=True)
    father_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=30, choices=PersonGender.choices, default=PersonGender.NOT_SPECIFIED)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    citizenship_status = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=150, blank=True)
    photo_file_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.full_name
