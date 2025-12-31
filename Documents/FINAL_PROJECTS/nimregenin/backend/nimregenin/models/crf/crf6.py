from django.db import models
from django.contrib.auth.models import User


class CRF6(models.Model):
    """Efficacy Assessment - One per scheduled visit"""
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf6')
    primary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    secondary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    clinician_global_impression = models.CharField(max_length=50, blank=True)
    patient_global_impression = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf6')
    visit_date = models.DateField(null=True, blank=True)
    # primary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    # secondary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    clinician_assessment = models.TextField(blank=True)

    def __str__(self):
        return f"CRF6 Efficacy - {self.visit}"

