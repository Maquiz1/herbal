from django.db import models
from core.models.queryset.site_queryset import SiteRestrictedQuerySet

class SiteRestrictedManager(models.Manager):

    def get_queryset(self):
        return SiteRestrictedQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)
