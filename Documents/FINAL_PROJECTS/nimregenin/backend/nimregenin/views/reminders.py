# nimregenin/views/reminders.py
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


import logging
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from nimregenin.models import Demographic, Visit

logger = logging.getLogger(__name__)


class VoiceReminderTwiMLView(View):
    """
    Generates dynamic TwiML for Twilio voice calls.
    Called by Twilio when a call is placed.
    """
    def get(self, request, site_code=None):
        today = timezone.now().date()
        grace_period = timedelta(days=7)

        resp = VoiceResponse()

        # Determine which visits to include
        if site_code:
            queryset = Visit.objects.filter(patient__site=site_code)
            site_name = dict(Demographic.SITE_CHOICES).get(site_code, 'your site')
        else:
            queryset = Visit.objects.all()
            site_name = "your sites"

        overdue_visits = queryset.filter(
            planned_date__lt=today - grace_period,
            completed=False
        ).select_related('patient')[:5]  # Limit for brevity

        if overdue_visits.exists():
            resp.say(
                "Hello, this is an automated voice reminder from the NIM Regenin clinical trial system.",
                voice='woman', language='en-US'
            )
            resp.say(
                f"There are {overdue_visits.count()} overdue visits at {site_name} as of {today.strftime('%B %d, %Y')}.",
                voice='woman'
            )
            resp.pause(length=1)

            for visit in overdue_visits:
                resp.say(
                    f"Patient {visit.patient.patient_id} has an overdue {visit.get_visit_type_display()} visit, "
                    f"planned for {visit.planned_date.strftime('%B %d')}.",
                    voice='woman'
                )

            if overdue_visits.count() == 5 and queryset.filter(planned_date__lt=today - grace_period, completed=False).count() > 5:
                resp.say("And additional overdue visits.", voice='woman')

            resp.say(
                "Please log in to the electronic data capture system as soon as possible to update these visits.",
                voice='woman'
            )
        else:
            resp.say(
                "This is the NIM Regenin system. There are currently no overdue visits requiring attention. Thank you.",
                voice='woman'
            )

        resp.say("This call was automated. Goodbye.", voice='woman')

        return HttpResponse(str(resp), content_type='application/xml')


# Optional: Keep management commands in commands/, but views here
# This file is only for HTTP views (TwiML webhook)

# class VoiceReminderTwiMLView(View):
#     def get(self, request, site_code=None):
#         today = timezone.now().date()
#         grace_period = timedelta(days=7)

#         resp = VoiceResponse()

#         if site_code:
#             overdue_visits = Visit.objects.filter(
#                 patient__site=site_code,
#                 planned_date__lt=today - grace_period,
#                 completed=False
#             ).select_related('patient')

#             site_name = dict(Demographic.SITE_CHOICES).get(site_code, 'your site')
#         else:
#             overdue_visits = Visit.objects.filter(
#                 planned_date__lt=today - grace_period,
#                 completed=False
#             )
#             site_name = "your sites"

#         if overdue_visits.exists():
#             resp.say(
#                 f"Hello, this is an automated voice reminder from the NIM Regenin clinical trial.",
#                 voice='woman', language='en-US'
#             )
#             resp.say(
#                 f"As of {today.strftime('%B %d, %Y')}, there are {overdue_visits.count()} overdue visits at {site_name}.",
#                 voice='woman'
#             )
#             resp.pause(length=1)

#             # List first few patients
#             for visit in overdue_visits[:3]:
#                 resp.say(
#                     f"Patient {visit.patient.patient_id} has an overdue {visit.get_visit_type_display()} visit, "
#                     f"planned for {visit.planned_date.strftime('%B %d')}.",
#                     voice='woman'
#                 )

#             if overdue_visits.count() > 3:
#                 resp.say(f"And {overdue_visits.count() - 3} more overdue visits.", voice='woman')

#             resp.say("Please log in to the EDC system immediately to update these visits.", voice='woman')
#         else:
#             resp.say("This is NIM Regenin system. There are currently no overdue visits. Thank you.", voice='woman')

#         resp.say("This call was automated. Goodbye.", voice='woman')

#         return HttpResponse(str(resp), content_type='text/xml')