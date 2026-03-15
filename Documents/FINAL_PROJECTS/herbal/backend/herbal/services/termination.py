# herbal/services/termination.py

from ..models import VisitSchedule


def terminate_subject(enrollment, termination_date):

    visits = VisitSchedule.objects.filter(enrollment=enrollment)

    for visit in visits:

        if visit.scheduled_date > termination_date:
            visit.status = "na"
            visit.save()
