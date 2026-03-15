# core/views/subject_visits.py


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.services.access_control import get_accessible_subjects


@login_required
def subject_detail_view(request, pk):

    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    return render(
        request,
        "herbal/subjects/subject_detail.html",
        {"subject": subject}
    )
