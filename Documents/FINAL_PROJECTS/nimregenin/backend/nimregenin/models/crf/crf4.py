from django.db import models
from django.contrib.auth.models import User



class CRF4(models.Model):
    """Adverse Events - Multiple allowed per visit"""
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf4_ae')
    ae_description = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')]
    )
    serious = models.BooleanField(default=False)
    onset_date = models.DateField()
    resolution_date = models.DateField(null=True, blank=True)
    outcome = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf4')
    visit_date = models.DateField(null=True, blank=True)
    # ae_description = models.TextField()
    # severity = models.CharField(max_length=20, choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')])
    # serious = models.BooleanField(default=False)
    # outcome = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"AE: {self.ae_description[:30]} - {self.visit}"
