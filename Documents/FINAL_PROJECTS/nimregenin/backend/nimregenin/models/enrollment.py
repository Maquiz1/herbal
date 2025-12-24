from django.db import models
from django.contrib.auth.models import User


class Enrollment(models.Model):
    patient = models.OneToOneField('nimregenin.Demographic', on_delete=models.CASCADE, related_name='enrollment')
    enrollment_date = models.DateField()
    study_id = models.CharField(max_length=50, blank=True)
    randomization_number = models.CharField(max_length=50, blank=True)
    STATUS_CHOICES = (
        ('ENROLLED', 'Enrolled'),
        ('RANDOMIZED', 'Randomized'),
        ('WITHDRAWN', 'Withdrawn'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ENROLLED')
    enrolled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Enrolled - {self.patient.participant_id}"