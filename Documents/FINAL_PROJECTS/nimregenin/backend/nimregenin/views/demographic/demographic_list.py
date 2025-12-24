"""
Patient Views: List, Detail (Visit), and Create/Update for Demographic model
"""

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

from ..create_update import CreateUpdateView
from ...models import (
    Demographic, Visit, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)


class PatientListView(LoginRequiredMixin, ListView):
    """
    Main patient registry list with visit status and overdue alerts.
    """
    model = Demographic
    template_name = 'nimregenin/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 25
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('visits')
        today = timezone.now().date()

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient_id__icontains=search) |
                Q(ethnicity__icontains=search) |
                Q(race__icontains=search)
            )

        # Annotate overdue visit count per patient
        for patient in queryset:
            overdue_count = 0
            for visit in patient.visits.all():
                if visit.planned_date:
                    grace_end = visit.planned_date + timedelta(days=7)
                    if today > grace_end and not visit.completed:
                        visit.is_overdue = True
                        overdue_count += 1
                    else:
                        visit.is_overdue = False
                else:
                    visit.is_overdue = False
            patient.overdue_visits = overdue_count

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        context['title'] = 'Patient Registry'
        context['total_patients'] = Demographic.objects.count()
        context['total_screened'] = Screening.objects.values('patient_id').distinct().count()
        context['total_enrolled'] = Enrollment.objects.values('patient_id').distinct().count()
        context['search_term'] = self.request.GET.get('search', '')

        # Overdue patient count for alert banner
        context['overdue_patient_count'] = Demographic.objects.filter(
            visits__planned_date__lt=today - timedelta(days=7),
            visits__completed=False
        ).distinct().count()

        return context

