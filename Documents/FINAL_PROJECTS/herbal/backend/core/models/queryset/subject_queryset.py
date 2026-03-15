from django.db import models


class SubjectQuerySet(models.QuerySet):

    def for_user(self, user):

        if user.is_superuser:
            return self

        profile = getattr(user, "staff_profile", None)

        if not profile:
            return self.none()

        role = profile.role

        if role in ["admin", "data_manager"]:
            return self

        if role in ["data_clerk", "coordinator"]:
            return self.filter(site=profile.site)

        if role in ["monitor", "reviewer", "pi"]:
            return self.filter(site__in=profile.assigned_sites.all())

        return self.none()
