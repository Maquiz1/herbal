from django.db import models


class SiteRestrictedQuerySet(models.QuerySet):

    def for_user(self, user):

        if user.is_superuser:
            return self

        profile = getattr(user, "staff_profile", None)

        if not profile:
            return self.none()

        role = profile.role

        # full access
        if role in ["admin", "data_manager"]:
            return self

        # single-site users
        if role in ["data_clerk", "coordinator"]:
            return self.filter(site=profile.site)

        # multi-site users
        if role in ["monitor", "reviewer", "pi"]:
            sites = profile.assigned_sites.all()

            if not sites.exists():
                return self.none()

            return self.filter(site__in=sites)

        return self.none()
