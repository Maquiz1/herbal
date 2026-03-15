# herbal/services/visit_timeline.py


from herbal.models import VisitSchedule


def get_subject_timeline(subject):

    enrollment = subject.enrollment

    visits = VisitSchedule.objects.filter(
        enrollment=enrollment
    ).order_by("scheduled_date")

    timeline = []

    for visit in visits:

        if visit.status == "completed":
            icon = "✔"

        elif visit.status == "na":
            icon = "N/A"

        elif visit.is_overdue():
            icon = "⚠"

        else:
            icon = "⏳"

        timeline.append({
            "visit_day": visit.visit_day,
            "scheduled_date": visit.scheduled_date,
            "status_icon": icon,
            "visit": visit
        })

    return timeline
