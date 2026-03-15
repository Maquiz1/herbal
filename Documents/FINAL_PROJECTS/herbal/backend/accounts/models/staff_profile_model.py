from django.db import models
from django.conf import settings
from herbal.models import Site


ROLE_CHOICES = [
    ("admin", "Admin"),
    ("data_manager", "Data Manager"),
    ("monitor", "Monitor"),
    ("coordinator", "Coordinator"),
    ("data_clerk", "Data Clerk"),
    ("reviewer", "Reviewer"),
    ("pi", "Principal Investigator"),
]


class StaffProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_staff"
    )

    assigned_sites = models.ManyToManyField(
        Site,
        blank=True,
        related_name="assigned_staff"
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.get_role_display()}"
