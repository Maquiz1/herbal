# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime, timedelta
from .. audit_model import AuditModel

class CRF4(AuditModel):
    """Concomitant Medications - One per visit (current list at that visit)"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf4'
    )
    visit_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when medication list was recorded"
    )
    no_conmeds = models.BooleanField(
        default=False,
        help_text="Check if patient is not taking any concomitant medications"
    )
    medications = models.TextField(
        blank=True,
        help_text="List all current medications: name, dose, frequency, indication"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "CRF4 - Concomitant Medications"
        verbose_name_plural = "CRF4 - Concomitant Medications"

    def __str__(self):
        pid = self.visit.enrollment.screening.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        return f"CRF4 ConMeds - {pid} ({self.visit_date|date:'M d, Y'|default:'No date'})"

