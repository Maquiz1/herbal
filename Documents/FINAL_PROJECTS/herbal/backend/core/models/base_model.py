# core/models/base_model.py

from django.db import models
from django.conf import settings
from .active_model import ActiveModel
from .audit_model import AuditModel
from .soft_delete_model import SoftDeleteModel

class BaseModel(
    AuditModel,
    ActiveModel,
    SoftDeleteModel
):

    class Meta:
        abstract = True

