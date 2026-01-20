from django.db import models
from django.contrib.auth.models import User
from . audit_model import AuditModel

class Screening(AuditModel):
    patient = models.OneToOneField('nimregenin.Patient', on_delete=models.CASCADE, related_name='screening')
    screening_date = models.DateField()
    STATUS_CHOICES = (
        ('PASS', 'Passed'),
        ('FAIL', 'Failed'),
        ('PENDING', 'Pending'),
    )
    screening_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Screening - {self.patient.pid}"