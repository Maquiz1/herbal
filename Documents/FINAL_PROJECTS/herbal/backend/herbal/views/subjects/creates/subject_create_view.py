from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from herbal.forms.subject_form import SubjectForm


@login_required
def subject_create_view(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            subject = form.save()

            return redirect("herbal:subjects-list")

    else:
        form = SubjectForm()

    return render(
        request,
        "herbal/subjects/subject_create.html",
        {"form": form},
    )
