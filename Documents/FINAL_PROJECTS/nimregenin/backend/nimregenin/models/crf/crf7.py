# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime, timedelta
from .. audit_model import AuditModel

class CRF7(AuditModel):
    """Efficacy Assessment - One per scheduled visit"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf7'
    )
    visit_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when efficacy was assessed"
    )
    primary_endpoint_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Primary efficacy endpoint score"
    )
    secondary_endpoint_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Secondary endpoint score"
    )
    clinician_global_impression = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clinician's global impression of change"
    )
    patient_global_impression = models.CharField(
        max_length=50,
        blank=True,
        help_text="Patient's global impression of change"
    )
    clinician_assessment = models.TextField(
        blank=True,
        help_text="Clinician's detailed assessment"
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
        verbose_name = "CRF7 - Efficacy Assessment"
        verbose_name_plural = "CRF7 - Efficacy Assessments"

    def __str__(self):
        pid = self.visit.enrollment.screening.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        date_str = self.visit_date.strftime("%b %d, %Y") if self.visit_date else "No date"
        return f"CRF7 Efficacy - {pid} ({date_str})"