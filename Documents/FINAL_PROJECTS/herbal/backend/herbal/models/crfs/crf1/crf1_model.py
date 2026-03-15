# herbal/models/crfs/crf1_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule

class CRF1(models.Model):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf1"
    )

    visit_date = models.DateField()

    weight = models.FloatField(null=True, blank=True)

    blood_pressure = models.CharField(max_length=20, blank=True)

    temperature = models.FloatField(null=True, blank=True)

    notes = models.TextField(blank=True)

