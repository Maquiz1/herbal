from django.db import models

class CRF7(models.Model):
    visit = models.OneToOneField('nimregenin.Visit', on_delete=models.CASCADE, related_name='crf7')
    completion_date = models.DateField(null=True, blank=True)
    early_termination = models.BooleanField(default=False)
    termination_reason = models.TextField(blank=True)
    study_completion_status = models.CharField(max_length=20, choices=[('COMPLETED', 'Completed'), ('TERMINATED', 'Terminated')], blank=True)

    def __str__(self):
        return f"CRF7 - {self.visit}"