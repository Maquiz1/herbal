from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):

    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted"
    )

    delete_reason = models.TextField(blank=True)

    objects = SoftDeleteManager()      # hides deleted records
    all_objects = models.Manager()     # includes deleted

    class Meta:
        abstract = True

    # MAIN SOFT DELETE METHOD
    def soft_delete(self, user=None, reason=None):

        if self.is_deleted:
            return

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user

        if reason:
            self.delete_reason = reason

        self.save(update_fields=[
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "delete_reason"
        ])

    # RESTORE RECORD
    def restore(self):

        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.delete_reason = ""

        self.save(update_fields=[
            "is_deleted",
            "deleted_at",
            "deleted_by",
            "delete_reason"
        ])

    # PREVENT HARD DELETE
    def delete(self, using=None, keep_parents=False):
        self.soft_delete()
