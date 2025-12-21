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
class DemographicListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/demographic_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demographics'] = Demographic.objects.all().order_by('-created_at')
        context['title'] = 'Patient Demographics'
        return context
    
class DemographicCreateUpdateView(CreateUpdateView):
    model = Demographic
    fields = ['patient_id', 'date_of_birth', 'age', 'gender', 'ethnicity', 'race']
    success_url_name = 'nimregenin:demographic_list'

# Screening
class ScreeningListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/screening_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['screenings'] = Screening.objects.all().order_by('-created_at')
        context['title'] = 'Screening Visits'
        return context
    
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