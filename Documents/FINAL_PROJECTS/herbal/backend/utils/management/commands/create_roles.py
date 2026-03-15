from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


ROLES = [
    "Admin",
    "Data Manager",
    "Monitor",
    "Coordinator",
    "Data Clerk",
    "Reviewer",
    "PI",
]


class Command(BaseCommand):

    help = "Create default user roles/groups"

    def handle(self, *args, **kwargs):

        created_count = 0

        for role in ROLES:

            group, created = Group.objects.get_or_create(name=role)

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created group: {role}"))
            else:
                self.stdout.write(self.style.WARNING(f"Group already exists: {role}"))

        self.stdout.write(self.style.SUCCESS(f"\n{created_count} new roles created."))
