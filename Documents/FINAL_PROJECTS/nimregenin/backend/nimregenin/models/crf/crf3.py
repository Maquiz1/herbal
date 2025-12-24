from django.db import models

class CRF3(models.Model):
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf3')
    visit_date = models.DateField(null=True, blank=True)
    hemoglobin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wbc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    platelets = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    creatinine = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alt = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    ast = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return f"CRF3 - {self.visit}"

