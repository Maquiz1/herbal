from django.db import models


class CRF2(models.Model):
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf2')
    visit_date = models.DateField(null=True, blank=True)
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    physical_exam_findings = models.TextField(blank=True)

    def __str__(self):
        return f"CRF2 - {self.visit}"
