# core/views/subject_visits.py

from django.shortcuts import render, get_object_or_404
from herbal.models import Subject
from herbal.services.visit_timeline import get_subject_timeline


def subject_dashboard(request, subject_id):

    subject = get_object_or_404(Subject, subject_id=subject_id)

    timeline = get_subject_timeline(subject)

    return render(
        request,
        "herbal/subject_dashboard.html",
        {
            "subject": subject,
            "timeline": timeline
        }
    )
