# herbal/models/enrollments/enrollment_model.py

from django.db import models
from ..subjects.subject_model import Subject


class Enrollment(models.Model):

    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name="enrollment"
    )

    enrollment_date = models.DateField()

    consent_signed = models.BooleanField(default=False)

    enrolled_by = models.CharField(max_length=100)

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("terminated", "Terminated"),
        ("lost", "Lost To Follow Up"),
        ("transfer", "Transferred Out"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    def __str__(self):
        return f"Enrollment - {self.subject}"
