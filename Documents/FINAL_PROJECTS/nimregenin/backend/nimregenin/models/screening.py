from django.db import models
from django.contrib.auth.models import User


class Screening(models.Model):
    patient = models.OneToOneField('nimregenin.Demographic', on_delete=models.CASCADE, related_name='screening')
    screening_date = models.DateField()
    STATUS_CHOICES = (
        ('PASS', 'Passed'),
        ('FAIL', 'Failed'),
        ('PENDING', 'Pending'),
    )
    screening_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True)
    screened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Screening - {self.patient.pid}"