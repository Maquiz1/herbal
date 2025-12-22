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



