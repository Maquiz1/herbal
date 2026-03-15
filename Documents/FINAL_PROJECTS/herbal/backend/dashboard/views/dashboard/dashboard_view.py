from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from herbal.models import Subject
from accounts.models import StaffProfile


@login_required
def dashboard_view(request):

    user = request.user
    profile = user.staff_profile
    role = profile.role

    subjects = Subject.objects.all()

    # Site-based filtering
    if role == "data_clerk" or role == "coordinator":
        subjects = subjects.filter(site=profile.site)

    elif role in ["monitor", "reviewer", "pi"]:
        subjects = subjects.filter(site__in=profile.assigned_sites.all())

    total_subjects = subjects.count()

    context = {
        "role": role,
        "subjects": subjects[:10],  # latest 10
        "total_subjects": total_subjects,
    }

    return render(request, "dashboard/dashboard.html", context)
