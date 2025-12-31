from django.db import models
from django.contrib.auth.models import User


class CRF2(models.Model):
    """Vital Signs - One per visit"""
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf2')
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf2')
    visit_date = models.DateField(null=True, blank=True)
    # systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    # diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    # heart_rate = models.PositiveIntegerField(null=True, blank=True)
    physical_exam_findings = models.TextField(blank=True)

    def __str__(self):
        return f"CRF2 Vital Signs - {self.visit}"
