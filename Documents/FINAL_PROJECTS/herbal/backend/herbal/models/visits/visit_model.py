from django.db import models
from core.models import BaseModel
from herbal.models.subjects.subject_model import Subject


VISIT_TYPES = [
    ("day0", "Day 0"),
    ("day7", "Day 7"),
    ("day14", "Day 14"),
    ("day30", "Day 30"),
    ("day60", "Day 60"),
    ("day90", "Day 90"),
    ("day120", "Day 120"),
    ("unscheduled", "Unscheduled"),
]


class Visit(BaseModel):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    visit_type = models.CharField(
        max_length=20,
        choices=VISIT_TYPES
    )

    scheduled_date = models.DateField()

    visit_date = models.DateField(
        null=True,
        blank=True
    )

    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject.subject_id} - {self.visit_type}"
