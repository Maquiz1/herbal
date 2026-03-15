# herbal/models/screening/screening_model.py

from django.db import models
from ..subjects.subject_model import Subject


class Screening(models.Model):

    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name="screening"
    )

    screening_date = models.DateField()

    age_eligible = models.BooleanField(default=False)

    inclusion_criteria_met = models.BooleanField(default=False)

    exclusion_criteria_present = models.BooleanField(default=False)

    eligible = models.BooleanField(default=False)

    comments = models.TextField(blank=True)

    def save(self, *args, **kwargs):

        self.eligible = (
            self.age_eligible
            and self.inclusion_criteria_met
            and not self.exclusion_criteria_present
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Screening - {self.patient}"
