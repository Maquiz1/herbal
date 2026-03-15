# herbal/models/crfs/crf1_model.py

from django.db import models

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)