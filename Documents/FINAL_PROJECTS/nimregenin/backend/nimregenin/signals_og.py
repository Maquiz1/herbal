from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Visit, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7


def get_required_crfs_for_visit(visit):
    """
    Returns a set of CRF model classes required for the given visit.
    """
    required = {CRF2, CRF3, CRF4, CRF5, CRF6}  # Common to all visits

    if visit.visit_type == 'BASELINE':
        required.add(CRF1)
    if visit.visit_type == 'DAY120':
        required.add(CRF7)

    return required


def update_visit_completion(visit):
    """
    Check if all required CRFs exist for the visit.
    If yes → mark visit.completed = True
    If no → mark False
    """
    required_models = get_required_crfs_for_visit(visit)

    all_filled = True
    for model in required_models:
        if not model.objects.filter(visit=visit).exists():
            all_filled = False
            break

    if all_filled != visit.completed:
        visit.completed = all_filled
        visit.save(update_fields=['completed'])


@receiver(post_save, sender=CRF1)
@receiver(post_save, sender=CRF2)
@receiver(post_save, sender=CRF3)
@receiver(post_save, sender=CRF4)
@receiver(post_save, sender=CRF5)
@receiver(post_save, sender=CRF6)
@receiver(post_save, sender=CRF7)
def on_crf_save(sender, instance, **kwargs):
    """
    Triggered when any CRF is saved.
    Updates the related visit's completion status.
    """
    if hasattr(instance, 'visit'):
        update_visit_completion(instance.visit)


@receiver(post_delete, sender=CRF1)
@receiver(post_delete, sender=CRF2)
@receiver(post_delete, sender=CRF3)
@receiver(post_delete, sender=CRF4)
@receiver(post_delete, sender=CRF5)
@receiver(post_delete, sender=CRF6)
@receiver(post_delete, sender=CRF7)
def on_crf_delete(sender, instance, **kwargs):
    """
    If a CRF is deleted, the visit should no longer be marked completed.
    """
    if hasattr(instance, 'visit'):
        update_visit_completion(instance.visit)