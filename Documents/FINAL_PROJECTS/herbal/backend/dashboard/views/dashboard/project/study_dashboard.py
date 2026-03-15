from django.shortcuts import render
from herbal.models import Subject


def study_dashboard(request):

    subjects = Subject.objects.select_related("enrollment")

    data = []

    for subject in subjects:

        visits = subject.enrollment.visits.all()

        visit_map = {v.visit_day: v for v in visits}

        data.append({
            "subject": subject,
            "visits": visit_map
        })

    return render(
        request,
        "herbal/study_dashboard.html",
        {
            "subjects": data
        }
    )
