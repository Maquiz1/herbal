# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User


class CRF2(models.Model):
    """Vital Signs - One per visit"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf2'
    )
    visit_date = models.DateField(null=True, blank=True, help_text="Date when vital signs were taken")
    systolic_bp = models.PositiveIntegerField(null=True, blank=True, help_text="mmHg")
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True, help_text="mmHg")
    heart_rate = models.PositiveIntegerField(null=True, blank=True, help_text="beats per minute")
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="°C"
    )
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, help_text="breaths per minute")
    physical_exam_findings = models.TextField(blank=True, help_text="Any notable physical exam findings")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "CRF2 - Vital Signs"
        verbose_name_plural = "CRF2 - Vital Signs"

    def __str__(self):
        pid = self.visit.enrollment.patient.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        date_str = self.visit_date.strftime("%b %d, %Y") if self.visit_date else "No date"
        return f"CRF2 Vital Signs - {pid} ({date_str})"