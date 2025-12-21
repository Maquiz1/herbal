from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from nimregenin.models import (
    Demographic, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)
# from backend.nimregenin.models import Visit
from django.db import models
from django.db.models import Q, Count
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from nimregenin.models import Demographic, Screening, Enrollment, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from nimregenin.models import Demographic, Visit, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

from django.utils import timezone
from datetime import timedelta

from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
import csv

from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from twilio.twiml.voice_response import VoiceResponse
from nimregenin.models import Visit
from .create_update import CreateUpdateView  # We'll create this base next

# Demographic
class PatientListView(LoginRequiredMixin, ListView):
    model = Demographic
    template_name = 'nimregenin/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 25
    ordering = ['-created_at']  # Newest first

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('visits')   
        today = timezone.now().date()  
           
        # Optional: Add search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient_id__icontains=search) |
                Q(ethnicity__icontains=search) |
                Q(race__icontains=search)
            )
            
        # Annotate each patient with overdue visit count
        for patient in queryset:
            overdue_count = 0
            for visit in patient.visits.all():
                if visit.planned_date and visit.planned_date < today and not visit.completed:
                    # Optional: add window tolerance, e.g., +7 days grace
                    grace_end = visit.planned_date + timedelta(days=7)
                    if today > grace_end:
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
        context['today'] = timezone.now().date()

        # Add summary stats for each patient (annotate)
        patients_with_stats = self.get_queryset().annotate(
            total_visits=Count('visits', distinct=True),
            completed_visits=Count('visits', filter=Q(visits__completed=True)),
            baseline_done=Count('visits', filter=Q(visits__visit_type='BASELINE', visits__completed=True)),
            day120_done=Count('visits', filter=Q(visits__visit_type='DAY120', visits__completed=True)),
        )
        # context['patients'] = patients_with_stats
        
        context['patients'] = self.get_queryset().annotate(
            total_expected_visits=Count('visits'),
            completed_visits=Count('visits', filter=models.Q(visits__completed=True)),
        )

        # Global stats for header
        # context['total_patients'] = Demographic.objects.count()
        # context['total_screened'] = Screening.objects.values('patient_id').distinct().count()
        # context['total_enrolled'] = Enrollment.objects.values('patient_id').distinct().count()

        # Search term
        context['search_term'] = self.request.GET.get('search', '')

        context['overdue_patient_count'] = Demographic.objects.filter(
            visits__planned_date__lt=today - timedelta(days=7),
            visits__completed=False
        ).distinct().count()
        
        context['overdue_patients'] = sum(1 for p in context['patients'] if getattr(p, 'overdue_visits', 0) > 0)
        return context

class PatientVisitDetailView(LoginRequiredMixin, DetailView):
    model = Visit
    template_name = 'nimregenin/patient_visit_detail.html'
    context_object_name = 'visit'
    pk_url_kwarg = 'visit_pk'

    def get_queryset(self):
        # Ensure user can only access visits for existing patients
        return Visit.objects.select_related('patient').prefetch_related(
            'crf1', 'crf2', 'crf3', 'crf4', 'crf5', 'crf6', 'crf7'
        )

    def get_object(self, queryset=None):
        patient_pk = self.kwargs.get('patient_pk')
        visit_pk = self.kwargs.get('visit_pk')
        
        # Security: ensure the visit belongs to the patient
        visit = get_object_or_404(Visit, patient__pk=patient_pk, pk=visit_pk)
        return visit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = self.object
        patient = visit.patient

        context['patient'] = patient

        # Gather CRF status
        context['crfs'] = {
            'baseline': {
                'name': 'CRF1 - Baseline Visit',
                'instance': getattr(visit, 'crf1', None),
                'exists': CRF1.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf1_create' if visit.visit_type == 'BASELINE' else None,
                'update_url': 'nimregenin:crf1_update',
                'delete_url': 'nimregenin:crf1_delete',
            },
            'physical_exam': {
                'name': 'CRF2 - Physical Examination',
                'instance': getattr(visit, 'crf2', None),
                'exists': CRF2.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf2_create',
                'update_url': 'nimregenin:crf2_update',
                'delete_url': 'nimregenin:crf2_delete',
            },
            'labs': {
                'name': 'CRF3 - Laboratory Results',
                'instance': getattr(visit, 'crf3', None),
                'exists': CRF3.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf3_create',
                'update_url': 'nimregenin:crf3_update',
                'delete_url': 'nimregenin:crf3_delete',
            },
            'con_meds': {
                'name': 'CRF4 - Concomitant Medications',
                'instance': getattr(visit, 'crf4', None),
                'exists': CRF4.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf4_create',
                'update_url': 'nimregenin:crf4_update',
                'delete_url': 'nimregenin:crf4_delete',
            },
            'adverse_events': {
                'name': 'CRF5 - Adverse Events',
                'instance': getattr(visit, 'crf5', None),
                'exists': CRF5.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf5_create',
                'update_url': 'nimregenin:crf5_update',
                'delete_url': 'nimregenin:crf5_delete',
            },
            'efficacy': {
                'name': 'CRF6 - Efficacy Assessment',
                'instance': getattr(visit, 'crf6', None),
                'exists': CRF6.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf6_create',
                'update_url': 'nimregenin:crf6_update',
                'delete_url': 'nimregenin:crf6_delete',
            },
            'completion': {
                'name': 'CRF7 - Study Completion/Termination',
                'instance': getattr(visit, 'crf7', None),
                'exists': CRF7.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf7_create' if visit.visit_type == 'DAY120' else None,
                'update_url': 'nimregenin:crf7_update',
                'delete_url': 'nimregenin:crf7_delete',
            },
        }

        # Visit status summary
        completed_crfs = sum(1 for c in context['crfs'].values() if c['exists'])
        total_expected = 6  # Adjust based on which CRFs are required per visit
        if visit.visit_type == 'BASELINE':
            total_expected += 1  # CRF1
        if visit.visit_type == 'DAY120':
            total_expected += 1  # CRF7

        context['crf_completion'] = f"{completed_crfs}/{total_expected}"

        return context
    
class DemographicCreateUpdateView(CreateUpdateView):
    model = Demographic
    fields = ['patient_id', 'date_of_birth', 'age', 'gender', 'ethnicity', 'race']
    success_url_name = 'nimregenin:demographic_list'
    
    def get_initial(self):
        initial = super().get_initial()
        visit_id = self.request.GET.get('visit')
        if visit_id:
            initial['visit'] = visit_id
        return initial

# Screening
class ScreeningListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/screening_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['screenings'] = Screening.objects.all().order_by('-created_at')
        context['title'] = 'Screening Visits'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        visit_id = self.request.GET.get('visit')
        if visit_id:
            initial['visit'] = visit_id
        return initial
    
class ScreeningCreateUpdateView(CreateUpdateView):
    model = Screening
    fields = ['patient_id', 'screening_date', 'screening_status', 'failure_reason', 'screened_by']
    success_url_name = 'nimregenin:screening_list'

# Enrollment
class EnrollmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/enrollment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.all().order_by('-created_at')
        context['title'] = 'Enrollment and Randomization'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        visit_id = self.request.GET.get('visit')
        if visit_id:
            initial['visit'] = visit_id
        return initial
    
class EnrollmentCreateUpdateView(CreateUpdateView):
    model = Enrollment
    fields = ['patient_id', 'enrollment_date', 'study_id', 'randomization_number', 'status', 'enrolled_by']
    success_url_name = 'nimregenin:enrollment_list'



