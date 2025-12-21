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

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Home page view - dashboard or welcome page after login.
    """
    template_name = 'nimregenin/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NIM Regenin Registry Dashboard'
        
        # Optional: Add some quick stats (example counts)
        from nimregenin.models import Demographic, Screening, Enrollment
        context['total_patients'] = Demographic.objects.count()
        context['screened_patients'] = Screening.objects.count()
        context['enrolled_patients'] = Enrollment.objects.count()
        
        return context

