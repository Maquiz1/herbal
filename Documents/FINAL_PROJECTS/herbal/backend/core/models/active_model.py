# core/models/active_model.py

from django.db import models

class ActiveModel(models.Model):

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
