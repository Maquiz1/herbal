from django.db import models
from django.contrib.auth.models import User


class CRF5(models.Model):
    """Concomitant Medications - One per visit (current list)"""
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf5')
    medication_name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100, blank=True)
    frequency = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    indication = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf5')
    visit_date = models.DateField(null=True, blank=True)
    # medication_name = models.CharField(max_length=200)
    # dose = models.CharField(max_length=100, blank=True)
    # start_date = models.DateField(null=True, blank=True)
    # end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"ConMed: {self.medication_name} - {self.visit}"
