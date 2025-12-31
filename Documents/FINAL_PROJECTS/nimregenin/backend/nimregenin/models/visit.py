from django.db import models


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

    patient = models.ForeignKey('nimregenin.Demographic', on_delete=models.CASCADE, related_name='visits')
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    planned_date = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('patient', 'visit_type')

    def __str__(self):
        return f"{self.get_visit_type_display()} - {self.patient.pid}"