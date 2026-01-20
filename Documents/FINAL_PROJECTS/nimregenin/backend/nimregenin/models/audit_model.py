from django.db import models
from django.contrib.auth.models import User


class AuditModel(models.Model):
    """
    Abstract base model to add audit fields to all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # prevent deleting users who created records
        null=False,
        blank=False,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # prevent deleting users who updated records
        null=False,
        blank=False,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            # 🔑 Only set created_by once
            if not self.pk and not self.created_by_id:
                self.created_by = user
            # 🔑 Always refresh updated_by
            self.updated_by = user

        super().save(*args, **kwargs)
