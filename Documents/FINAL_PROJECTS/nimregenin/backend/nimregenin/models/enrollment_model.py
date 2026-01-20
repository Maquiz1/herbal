from django.db import models
from . audit_model import AuditModel

class Enrollment(AuditModel):
    screening = models.OneToOneField('nimregenin.Screening', on_delete=models.CASCADE, related_name='enrollment')
    enrollment_date = models.DateField()
    study_id = models.CharField(max_length=50, blank=True)
    randomization_number = models.CharField(max_length=50, blank=True)
    STATUS_CHOICES = (
        ('ENROLLED', 'Enrolled'),
        ('RANDOMIZED', 'Randomized'),
        ('WITHDRAWN', 'Withdrawn'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ENROLLED')

    def __str__(self):
        if self.screening and self.screening.patient:
            return f"Enrollment - {self.screening.patient.pid} ({self.screening.patient.get_full_name()})"
        return "Enrollment (no patient)"
