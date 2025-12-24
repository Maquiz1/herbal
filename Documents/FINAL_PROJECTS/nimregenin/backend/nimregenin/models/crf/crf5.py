from django.db import models


class CRF5(models.Model):
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf5')
    visit_date = models.DateField(null=True, blank=True)
    medication_name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"CRF5 Med - {self.visit}"
