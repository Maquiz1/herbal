# herbal/services/visit_scheduler.py

from datetime import timedelta
from constants.constants import VISIT_SCHEDULE
from ..models import VisitSchedule


def generate_visit_schedule(enrollment):

    enrollment_date = enrollment.enrollment_date

    for visit_day, offset in VISIT_SCHEDULE.items():

        scheduled_date = enrollment_date + timedelta(days=offset)

        visit, created = VisitSchedule.objects.get_or_create(
            enrollment=enrollment,
            visit_day=visit_day
        )

        if visit.status != "completed":
            visit.scheduled_date = scheduled_date
            visit.save()

