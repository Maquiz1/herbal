# sites/models/site_model.py

from django.db import models
from datetime import date

class Site(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4)  

    def __str__(self):
        return f"{self.name} - {self.code}"

