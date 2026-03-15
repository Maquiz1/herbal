# herbal/models/crfs/crf6_model.py

from django.db import models
from ...enrollments.enrollment_model import Enrollment

class CRF6(models.Model):

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="termination"
    )

    termination_date = models.DateField()

    reason = models.CharField(
        max_length=50,
        choices=[
            ("completed","Completed Study"),
            ("lost_follow_up","Lost To Follow Up"),
            ("withdrawn","Participant Withdrew"),
            ("transfer_out","Transferred Out"),
            ("medical_reason","Medical Reason"),
        ]
    )

    comments = models.TextField(blank=True)
