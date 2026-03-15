# herbal/models/crfs/crf3_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule



class CRF3(models.Model):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf3"
    )

    symptoms = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=[
            ("mild","Mild"),
            ("moderate","Moderate"),
            ("severe","Severe")
        ]
    )

    notes = models.TextField(blank=True)
