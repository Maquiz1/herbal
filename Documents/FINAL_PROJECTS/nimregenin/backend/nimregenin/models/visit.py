# nimregenin/models/visit.py

from django.db import models
from django.contrib.auth.models import User


class Visit(models.Model):
    VISIT_TYPES = (
        ('BASELINE', 'Baseline (Day 0)'),
        ('DAY7', 'Day 7'),
        ('DAY14', 'Day 14'),
        ('DAY30', 'Day 30'),
        ('DAY60', 'Day 60'),
        ('DAY90', 'Day 90'),
        ('DAY120', 'Day 120'),
    )

    enrollment = models.ForeignKey(                 # ← Must be 'enrollment'
            'nimregenin.Enrollment',
            on_delete=models.CASCADE,
            related_name='visits'
        )
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    planned_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('enrollment', 'visit_type')
        ordering = ['planned_date']

    def __str__(self):
        # Safe access: Enrollment → Screening → Demographic → pid
        if hasattr(self.enrollment, 'patient') and hasattr(self.enrollment.patient, 'patient'):
            return f"{self.get_visit_type_display()} - {self.enrollment.patient.patient.pid}"
        return f"{self.get_visit_type_display()} - (No PID)"