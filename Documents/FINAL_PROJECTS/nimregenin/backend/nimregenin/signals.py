# nimregenin/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Enrollment, Visit

@receiver(pre_save, sender=Enrollment)
def track_enrollment_date_change(sender, instance, **kwargs):
    if instance.pk:
        # On update, check if date changed
        old_instance = Enrollment.objects.get(pk=instance.pk)
        instance._old_enrollment_date = old_instance.enrollment_date
    else:
        instance._old_enrollment_date = None

@receiver(post_save, sender=Enrollment)
def manage_visit_schedule(sender, instance, created, **kwargs):
    enrollment_date = instance.enrollment_date
    enrolled_by = instance.enrolled_by

    visit_schedule = [
        ('BASELINE', 0),
        ('DAY7', 7),
        ('DAY14', 14),
        ('DAY30', 30),
        ('DAY60', 60),
        ('DAY90', 90),
        ('DAY120', 120),
    ]

    if created:
        # On create: generate all visits
        for visit_type, days_offset in visit_schedule:
            planned_date = enrollment_date + timedelta(days=days_offset)
            Visit.objects.create(
                enrollment=instance,
                visit_type=visit_type,
                planned_date=planned_date,
                created_by=enrolled_by
            )
    elif instance._old_enrollment_date and instance._old_enrollment_date != enrollment_date:
        # On update: if date changed, adjust all planned dates
        date_diff = (enrollment_date - instance._old_enrollment_date).days
        visits = instance.visits.all()
        for visit in visits:
            if visit.planned_date:
                visit.planned_date += timedelta(days=date_diff)
            visit.save()