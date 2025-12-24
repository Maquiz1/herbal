from django.db import models


class CRF6(models.Model):
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf6')
    visit_date = models.DateField(null=True, blank=True)
    primary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    secondary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    clinician_assessment = models.TextField(blank=True)

    def __str__(self):
        return f"CRF6 - {self.visit}"

