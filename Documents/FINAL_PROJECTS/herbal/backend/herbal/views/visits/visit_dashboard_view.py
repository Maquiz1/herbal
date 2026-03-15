from django.shortcuts import render
from django.utils import timezone

from herbal.models.visits.visit_schedule_model import VisitSchedule


def visit_dashboard_view(request):

    today = timezone.now().date()

    visits = VisitSchedule.objects.select_related(
        "enrollment",
        "enrollment__subject"
    )

    due_today = visits.filter(
        scheduled_date=today,
        status="pending"
    )

    overdue = visits.filter(
        scheduled_date__lt=today,
        status="pending"
    )

    upcoming = visits.filter(
        scheduled_date__gt=today,
        status="pending"
    )

    completed = visits.filter(
        status="completed"
    )

    context = {
        "due_today": due_today,
        "overdue": overdue,
        "upcoming": upcoming,
        "completed": completed,

        "due_today_count": due_today.count(),
        "overdue_count": overdue.count(),
        "upcoming_count": upcoming.count(),
        "completed_count": completed.count(),
    }

    return render(
        request,
        "herbal/visits/visit_dashboard.html",
        context
    )
