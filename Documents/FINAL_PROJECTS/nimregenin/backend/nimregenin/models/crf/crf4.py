from django.db import models



class CRF4(models.Model):
    visit = models.ForeignKey('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf4')
    visit_date = models.DateField(null=True, blank=True)
    ae_description = models.TextField()
    severity = models.CharField(max_length=20, choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')])
    serious = models.BooleanField(default=False)
    outcome = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"CRF4 AE - {self.visit}"
