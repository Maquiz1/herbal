# herbal/models/subjects/subject_model.py
# herbal/models/subjects/subject_model.py

from django.db import models
from datetime import date

from sites.models import Site
from core.models import BaseModel
from core.managers.site_manager import SiteRestrictedManager


class Subject(BaseModel):

    subject_id = models.CharField(max_length=50, unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    sex = models.CharField(
        max_length=10, choices=[("Male", "Male"), ("Female", "Female")]
    )

    date_of_birth = models.DateField()

    phone = models.CharField(max_length=20, blank=True, null=True)

    village = models.CharField(max_length=100, blank=True)

    registration_date = models.DateField(auto_now_add=True)

    site = models.ForeignKey(Site, on_delete=models.PROTECT)

    # site-aware manager
    objects = SiteRestrictedManager()

    def age(self):

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


    @property
    def status(self):

        if hasattr(self, "enrollment") and self.enrollment:
            return "enrolled"

        if hasattr(self, "screening") and self.screening:
            return "screened"

        return "registered"

    @property
    def progress(self):

        status_map = {
            "registered": 20,
            "screened": 40,
            "enrolled": 60,
            "followup": 80,
            "completed": 100,
        }

        return status_map.get(self.status, 0)

    def __str__(self):

        return f"{self.subject_id} - {self.first_name} {self.last_name}"
