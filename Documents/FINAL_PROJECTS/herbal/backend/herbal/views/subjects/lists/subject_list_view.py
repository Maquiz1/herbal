# herbal/views/subjects/list/subject_list_view.py

from django.shortcuts import render
from django.core.paginator import Paginator

from herbal.services.access_control import get_accessible_subjects


def subject_list_view(request):

    subjects = get_accessible_subjects(request.user)

    # SEARCH
    search = request.GET.get("search")

    if search:
        subjects = subjects.filter(subject_id__icontains=search)

    # FILTER STATUS
    status = request.GET.get("status")

    if status == "registered":
        subjects = subjects.filter(
            is_active=True,
            # screening__isnull=True
        )

    elif status == "screened":
        subjects = subjects.filter(
            screening__isnull=False,
            # enrollment__isnull=True
        )

    elif status == "enrolled":
        subjects = subjects.filter(
            enrollment__isnull=False
        )


    # PAGINATION
    paginator = Paginator(subjects, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
        "status": status,
        "subjects":subjects
    }

    return render(
        request,
        "herbal/subjects/subject_list.html",
        context
    )
