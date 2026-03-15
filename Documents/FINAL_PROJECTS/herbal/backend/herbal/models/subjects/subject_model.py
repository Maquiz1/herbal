# herbal/models/subjects/subject_model.py

from django.db import models
from datetime import date
from sites.models import Site
from core.models import BaseModel


class Subject(BaseModel):

    subject_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    sex = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")]
    )
    
    date_of_birth = models.DateField()
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True)
    registration_date = models.DateField(auto_now_add=True)

    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year

    def __str__(self):
        return f"{self.study_id} - {self.first_name} {self.last_name}"
