# nimregenin/models/crf.py

from django.db import models
from django.contrib.auth.models import User
from .. audit_model import AuditModel

class CRF3(AuditModel):
    """Laboratory Results - One per visit"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf3'
    )
    visit_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when lab samples were taken"
    )
    hemoglobin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="g/dL"
    )
    wbc = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="×10³/µL"
    )
    platelets = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="×10³/µL"
    )
    creatinine = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="mg/dL"
    )
    alt = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="U/L"
    )
    ast = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="U/L"
    )
    notes = models.TextField(
        blank=True,
        help_text="Any additional lab notes or comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "CRF3 - Laboratory Results"
        verbose_name_plural = "CRF3 - Laboratory Results"

    def __str__(self):
        pid = self.visit.enrollment.screening.patient.pid if hasattr(self.visit, 'enrollment') else "Unknown"
        date_str = self.visit_date.strftime("%b %d, %Y") if self.visit_date else "No date"
        return f"CRF3 Labs - {pid} ({date_str})"