from django.db import models
from django.contrib.auth.models import User

class CRF7(models.Model):
    """Study Completion / Early Termination - Only once, at end of study"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf7',
        limit_choices_to={'visit_type__in': ['DAY120']}  # Or handle in view logic
    )
    completion_date = models.DateField()
    TERMINATION_CHOICES = (
        ('COMPLETED', 'Completed 120 Days Follow-Up'),
        ('DEATH', 'Patient Died'),
        ('WITHDRAWN', 'Withdrew Consent'),
        ('LTFU', 'Lost to Follow-Up'),
        ('OTHER', 'Other'),
    )
    termination_reason = models.CharField(max_length=20, choices=TERMINATION_CHOICES)
    other_reason = models.TextField(blank=True)
    final_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf7')
    # completion_date = models.DateField(null=True, blank=True)
    early_termination = models.BooleanField(default=False)
    # termination_reason = models.TextField(blank=True)
    study_completion_status = models.CharField(max_length=20, choices=[('COMPLETED', 'Completed'), ('TERMINATED', 'Terminated')], blank=True)

    def __str__(self):
        return f"CRF7 Completion - {self.visit.enrollment.patient.patient.pid}"