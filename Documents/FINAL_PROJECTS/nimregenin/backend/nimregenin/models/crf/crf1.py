from django.db import models


class CRF1(models.Model):
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf1')
    visit_date = models.DateField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    medical_history = models.TextField(blank=True)
    concomitant_medications = models.TextField(blank=True)

    def __str__(self):
        return f"CRF1 - {self.visit}"
