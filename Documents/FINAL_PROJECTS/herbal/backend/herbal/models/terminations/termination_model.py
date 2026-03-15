# nimregenin/models/end_of_study.py

from django.db import models
from .enrollment import Enrollment


class EndOfStudy(models.Model):

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="end_of_study"
    )

    eos_date = models.DateField()

    REASON_CHOICES = [
        ("completed", "Completed Study"),
        ("terminated", "Early Termination"),
        ("lost", "Lost to Follow Up"),
        ("transfer", "Transferred Out"),
    ]

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)

    comments = models.TextField(blank=True)

    def __str__(self):
        return f"End of Study - {self.enrollment.patient}"
