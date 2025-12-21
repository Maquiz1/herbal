from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import (
    Demographic, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)
# from backend.nimregenin.models import Visit
from django.db import models
from django.db.models import Q, Count
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from .models import Demographic, Screening, Enrollment, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Demographic, Visit, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

from django.utils import timezone
from datetime import timedelta

from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
import csv

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Home page view - dashboard or welcome page after login.
    """
    template_name = 'nimregenin/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NIM Regenin Registry Dashboard'
        
        # Optional: Add some quick stats (example counts)
        from .models import Demographic, Screening, Enrollment
        context['total_patients'] = Demographic.objects.count()
        context['screened_patients'] = Screening.objects.count()
        context['enrolled_patients'] = Enrollment.objects.count()
        
        return context


class CreateUpdateView(LoginRequiredMixin, View):
    """
    Generic view that handles both Create and Update in one view.
    - If pk is provided → Update
    - If no pk → Create
    """
    model = None
    fields = None
    template_name = 'nimregenin/form.html'
    success_url_name = None  # e.g., 'nimregenin:demographic_list'

    def get_object(self, pk=None):
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return None

    def get(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form(obj)
        return self.render_form(form, obj)

    def post(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form(obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        return self.render_form(form, obj)

    def get_form(self, obj=None, data=None):
        if self.fields:
            return self.modelform_class(data or None, instance=obj)
        return self.modelform_class(data or None, instance=obj)

    def render_form(self, form, obj=None):
        context = {
            'form': form,
            'object': obj,
            'title': f"{'Edit' if obj else 'Create'} {self.model._meta.verbose_name}",
        }
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy(self.success_url_name)

    # To make it work with Django's form handling
    modelform_class = None

    @classmethod
    def as_view(cls, **initkwargs):
        # Dynamically set the form class if not provided
        if 'modelform_class' not in initkwargs:
            initkwargs['modelform_class'] = type(
                f"{cls.model.__name__}Form",
                (forms.ModelForm,),
                {'Meta': {'model': cls.model, 'fields': cls.fields or '__all__'}}
            )
        return super().as_view(**initkwargs)

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
            },
            'physical_exam': {
                'name': 'CRF2 - Physical Examination',
                'instance': getattr(visit, 'crf2', None),
                'exists': CRF2.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf2_create',
                'update_url': 'nimregenin:crf2_update',
            },
            'labs': {
                'name': 'CRF3 - Laboratory Results',
                'instance': getattr(visit, 'crf3', None),
                'exists': CRF3.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf3_create',
                'update_url': 'nimregenin:crf3_update',
            },
            'con_meds': {
                'name': 'CRF4 - Concomitant Medications',
                'instance': getattr(visit, 'crf4', None),
                'exists': CRF4.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf4_create',
                'update_url': 'nimregenin:crf4_update',
            },
            'adverse_events': {
                'name': 'CRF5 - Adverse Events',
                'instance': getattr(visit, 'crf5', None),
                'exists': CRF5.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf5_create',
                'update_url': 'nimregenin:crf5_update',
            },
            'efficacy': {
                'name': 'CRF6 - Efficacy Assessment',
                'instance': getattr(visit, 'crf6', None),
                'exists': CRF6.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf6_create',
                'update_url': 'nimregenin:crf6_update',
            },
            'completion': {
                'name': 'CRF7 - Study Completion/Termination',
                'instance': getattr(visit, 'crf7', None),
                'exists': CRF7.objects.filter(visit=visit).exists(),
                'create_url': 'nimregenin:crf7_create' if visit.visit_type == 'DAY120' else None,
                'update_url': 'nimregenin:crf7_update',
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

# CRFs (example for CRF1; repeat pattern for others)
class CRF1ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf1_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf1_records'] = CRF1.objects.all().order_by('-created_at')
        context['title'] = 'CRF1 - Baseline Assessment'
        return context
    
class CRF1CreateUpdateView(CreateUpdateView):
    model = CRF1
    fields = '__all__'
    success_url_name = 'nimregenin:crf1_list'

# CRF2
class CRF2ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf2_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf2_records'] = CRF2.objects.all().order_by('-created_at')
        context['title'] = 'CRF2 - Follow-up Visit'
        return context
    
class CRF2CreateUpdateView(CreateUpdateView):
    model = CRF2
    fields = '__all__'
    success_url_name = 'nimregenin:crf2_list'

# Repeat for CRF3
class CRF3ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf3_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf3_records'] = CRF3.objects.all().order_by('-created_at')
        context['title'] = 'CRF3 - Adverse Events'
        return context
    
class CRF3CreateUpdateView(CreateUpdateView):
    model = CRF3
    fields = '__all__'
    success_url_name = 'nimregenin:crf3_list'

class CRF4ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf4_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf4_records'] = CRF4.objects.all().order_by('-created_at')
        context['title'] = 'CRF4 - Laboratory Results'
        return context
    
class CRF4CreateUpdateView(CreateUpdateView):
    model = CRF4
    fields = '__all__'
    success_url_name = 'nimregenin:crf4_list'
    
class CRF5ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf5_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf5_records'] = CRF5.objects.all().order_by('-created_at')
        context['title'] = 'CRF5 - Medication Administration'
        return context
    
class CRF5CreateUpdateView(CreateUpdateView):
    model = CRF5
    fields = '__all__'
    success_url_name = 'nimregenin:crf5_list'
    
class CRF6ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf6_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf6_records'] = CRF6.objects.all().order_by('-created_at')
        context['title'] = 'CRF6 - Efficacy Assessment'
        return context

class CRF7ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf7_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf7_records'] = CRF7.objects.all().order_by('-created_at')
        context['title'] = 'CRF7 - Study Completion / Early Termination'
        return context
    
class CRF6CreateUpdateView(CreateUpdateView):
    model = CRF6
    fields = '__all__'
    success_url_name = 'nimregenin:crf6_list'

class CRF7ListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/crf7_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf7_records'] = CRF7.objects.all().order_by('-created_at')
        context['title'] = 'CRF7 - Study Completion / Early Termination'
        return context  
    
class CRF7CreateUpdateView(CreateUpdateView):
    model = CRF7
    fields = '__all__'
    success_url_name = 'nimregenin:crf7_list'

class OverduePatientsCSVExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        grace_period = timedelta(days=7)  # 7-day window after planned date

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="overdue_patients_{}.csv"'.format(today.strftime('%Y%m%d'))

        writer = csv.writer(response)
        writer.writerow([
            'Patient ID', 'Age', 'Gender', 'Enrollment Date',
            'Visit Type', 'Planned Date', 'Actual Date', 'Days Overdue', 'Status'
        ])

        overdue_patients = Demographic.objects.filter(visits__planned_date__lt=today - grace_period, visits__completed=False).distinct()

        for patient in overdue_patients.prefetch_related('visits', 'enrollment'):
            enrollment_date = getattr(patient.enrollment, 'enrollment_date', 'N/A')

            for visit in patient.visits.all():
                if visit.planned_date and (visit.planned_date + grace_period) < today and not visit.completed:
                    days_overdue = (today - (visit.planned_date + grace_period)).days
                    status = 'Overdue'

                    writer.writerow([
                        patient.patient_id,
                        patient.age or 'N/A',
                        patient.get_gender_display() or 'N/A',
                        enrollment_date,
                        visit.get_visit_type_display(),
                        visit.planned_date,
                        visit.actual_date or 'Not occurred',
                        days_overdue,
                        status
                    ])

        return response