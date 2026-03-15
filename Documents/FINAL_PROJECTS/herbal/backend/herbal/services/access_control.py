# herbal/services/access_control.py

from herbal.models import Subject
from utils.permissions import *


def get_accessible_subjects(user):

    qs = Subject.objects.all()

    # SUPERUSER ALWAYS SEES EVERYTHING
    if user.is_superuser:
        return qs

    # GLOBAL ACCESS ROLES
    if is_admin(user) or is_data_manager(user):
        return qs

    # Get staff profile safely
    profile = getattr(user, "staff_profile", None)

    if not profile:
        return qs.none()

    # SITE-RESTRICTED ROLES
    if is_data_clerk(user) or is_coordinator(user):
        return qs.filter(site=profile.site)

    # MULTI-SITE ROLES
    if is_reviewer(user) or is_monitor(user) or is_pi(user):
        return qs.filter(site__in=profile.assigned_sites.all())

    return qs.none()
