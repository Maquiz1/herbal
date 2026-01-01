# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime, timedelta


class CRF5(models.Model):
    """Adverse Events - Multiple allowed per visit"""
    visit = models.ForeignKey(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf5_aes'
    )
    visit_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when AE was reported"
    )
    ae_description = models.TextField(help_text="Description of the adverse event")
    severity = models.CharField(
        max_length=20,
        choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')],
        help_text="Severity grade"
    )
    serious = models.BooleanField(default=False, help_text="Is this a Serious Adverse Event?")
    onset_date = models.DateField(help_text="Date AE started")
    resolution_date = models.DateField(null=True, blank=True, help_text="Date AE resolved (if applicable)")
    outcome = models.CharField(max_length=50, blank=True, help_text="Outcome of the AE")
    relationship_to_study = models.CharField(
        max_length=20,
        choices=[
            ('RELATED', 'Related'),
            ('POSSIBLY_RELATED', 'Possibly Related'),
            ('NOT_RELATED', 'Not Related'),
            ('UNKNOWN', 'Unknown')
        ],
        blank=True
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
        verbose_name = "CRF5 - Adverse Event"
        verbose_name_plural = "CRF5 - Adverse Events"
        ordering = ['-onset_date']

    def __str__(self):
        pid = self.visit.enrollment.patient.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        return f"AE: {self.ae_description[:40]} - {pid}"