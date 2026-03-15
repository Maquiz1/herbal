# herbal/models/visits/visit_schedule_model.py

from django.db import models
from ..enrollments.enrollment_model import Enrollment
from django.utils import timezone


VISIT_DAY_CHOICES = [
    ("D0", "Day 0"),
    ("D7", "Day 7"),
    ("D14", "Day 14"),
    ("D30", "Day 30"),
    ("D60", "Day 60"),
    ("D90", "Day 90"),
    ("D120", "Day 120"),
]


class VisitSchedule(models.Model):

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    visit_day = models.CharField(max_length=10, choices=VISIT_DAY_CHOICES)

    scheduled_date = models.DateField()

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("missed", "Missed"),
        ("na", "Not Applicable"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    actual_visit_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["scheduled_date"]

    def is_overdue(self):
        if self.status == "pending" and self.scheduled_date < timezone.now().date():
            return True
        return False

    def __str__(self):
        return f"{self.enrollment.subject.subject_id} - {self.visit_day}"
