# herbal/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Enrollment
from .services.visit_scheduler import generate_visit_schedule


@receiver(post_save, sender=Enrollment)
def create_visit_schedule(sender, instance, created, **kwargs):

    generate_visit_schedule(instance)
