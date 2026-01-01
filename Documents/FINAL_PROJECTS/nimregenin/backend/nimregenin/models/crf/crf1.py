from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class CRF1(models.Model):
    """Baseline Assessment - Only for Baseline visit"""
    visit = models.OneToOneField(
        'nimregenin.Visit',
        on_delete=models.CASCADE,
        related_name='crf1',
        limit_choices_to={'visit_type': 'BASELINE'}
    )
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, editable=False)
    medical_history = models.TextField(blank=True)
    baseline_conmeds = models.TextField(blank=True, help_text="List of concomitant medications at baseline")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf1')
    visit_date = models.DateField(null=True, blank=True)
    # height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    # medical_history = models.TextField(blank=True)
    concomitant_medications = models.TextField(blank=True)
    
    # def save(self, *args, **kwargs):
    #     if self.height_cm and self.weight_kg:
    #         self.bmi = round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)
    #     super().save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if self.height_cm and self.weight_kg and self.height_cm > 0:
            height_m = Decimal(self.height_cm) / 100
            self.bmi = round(Decimal(self.weight_kg) / (height_m ** 2), 1)
        else:
            self.bmi = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CRF1 Baseline - {self.visit.enrollment.patient.patient.pid}"
