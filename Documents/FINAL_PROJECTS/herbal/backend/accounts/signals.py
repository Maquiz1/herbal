from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import StaffProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):

    if created:
        StaffProfile.objects.create(user=instance)
