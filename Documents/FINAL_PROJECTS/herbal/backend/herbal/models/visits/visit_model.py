# herbal/models/visits/visit_model.py

from django.db import models
from .visit_schedule_model import VisitSchedule


class Visit(models.Model):

    schedule = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="visit"
    )

    visit_date = models.DateField()

    weight = models.FloatField(blank=True, null=True)

    blood_pressure = models.CharField(max_length=20, blank=True)

    symptoms = models.TextField(blank=True)

    adverse_events = models.TextField(blank=True)

    def __str__(self):
        return f"Visit {self.schedule.visit_day}"
