# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime, timedelta

class CRF6(models.Model):
    """Study Completion / Early Termination - Only once, at end of study"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf6',
        limit_choices_to={'visit_type__in': ['DAY120']}  # Enforced in DB
    )
    completion_date = models.DateField(help_text="Date of final visit or termination")
    early_termination = models.BooleanField(
        default=False,
        help_text="Check if patient exited study before Day 120"
    )
    TERMINATION_CHOICES = (
        ('COMPLETED', 'Completed 120 Days Follow-Up'),
        ('DEATH', 'Patient Died'),
        ('WITHDRAWN', 'Withdrew Consent'),
        ('LTFU', 'Lost to Follow-Up'),
        ('OTHER', 'Other'),
    )
    termination_reason = models.CharField(
        max_length=20,
        choices=TERMINATION_CHOICES,
        blank=True,
        help_text="Required if early termination"
    )
    other_reason = models.TextField(
        blank=True,
        help_text="Specify if 'Other' selected"
    )
    study_completion_status = models.CharField(
        max_length=20,
        choices=[
            ('COMPLETED', 'Completed'),
            ('TERMINATED', 'Terminated')
        ],
        help_text="Final study status"
    )
    final_notes = models.TextField(blank=True, help_text="Any final comments")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "CRF6 - Study Completion/Termination"
        verbose_name_plural = "CRF6 - Study Completion/Termination"

    def __str__(self):
        pid = self.visit.enrollment.patient.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        return f"CRF6 Completion - {pid} ({self.completion_date|date:'M d, Y'})"
