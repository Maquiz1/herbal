# herbal/models/crfs/crf7_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule

class CRF7(models.Model):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf7"
    )

    investigator_notes = models.TextField()

    follow_up_needed = models.BooleanField(default=False)

