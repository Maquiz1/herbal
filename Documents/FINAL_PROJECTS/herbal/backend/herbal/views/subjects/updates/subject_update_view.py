from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from herbal.forms.subject_form import SubjectForm
from herbal.services.access_control import get_accessible_subjects


@login_required
def subject_update_view(request, pk):

    subjects = get_accessible_subjects(request.user)

    subject = get_object_or_404(subjects, pk=pk)

    if request.method == "POST":

        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            return redirect("herbal:subjects-detail", pk=subject.pk)

    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "herbal/subjects/subject_update.html",
        {
            "form": form,
            "subject": subject
        }
    )
