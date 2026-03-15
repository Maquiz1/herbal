# herbal/views/subjects/list/subject_list_view.py

from django.shortcuts import render
from herbal.models import Subject
from utils.pagination import paginate_queryset
from utils.filters import apply_search, apply_filters
from sites.models import Site


def subject_list_view(request):

    subjects = Subject.objects.for_user(request.user)

    search = request.GET.get("search")
    status = request.GET.get("status")

    # SEARCH
    subjects = apply_search(
        subjects,
        search,
        ["subject_id", "first_name", "last_name", "phone"]
    )

    # SITE FILTER
    subjects = apply_filters(subjects, request, ["site"])

    # -------- COUNTS BEFORE STATUS FILTER --------
    total_subjects = subjects.count()

    registered_count = subjects.filter(is_active=True).count()

    screened_count = subjects.filter(
        screening__isnull=False
    ).count()

    enrolled_count = subjects.filter(
        enrollment__isnull=False
    ).count()
    # ---------------------------------------------

    # STATUS FILTER (for table)
    if status == "registered":
        subjects = subjects.filter(is_active=True)

    elif status == "screened":
        subjects = subjects.filter(screening__isnull=False)

    elif status == "enrolled":
        subjects = subjects.filter(enrollment__isnull=False)

    page_obj = paginate_queryset(request, subjects)

    sites = Site.objects.all()

    context = {
        "page_obj": page_obj,
        "search": search,
        "status": status,
        "sites": sites,

        # counts
        "total_subjects": total_subjects,
        "registered_count": registered_count,
        "screened_count": screened_count,
        "enrolled_count": enrolled_count,
    }

    return render(
        request,
        "herbal/subjects/subject_list.html",
        context
    )
