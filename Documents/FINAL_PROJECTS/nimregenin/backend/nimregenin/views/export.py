from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from nimregenin.models import (
    Patient, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)
# from backend.nimregenin.models import Visit
from django.db import models
from django.db.models import Q, Count
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from nimregenin.models import Patient, Screening, Enrollment, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from nimregenin.models import Patient, Visit, CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7

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

        overdue_patients = Patient.objects.filter(visits__planned_date__lt=today - grace_period, visits__completed=False).distinct()

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
    

