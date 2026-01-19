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

from ..create_update_view import CreateUpdateView
from ...models import (
    Demographic, Visit, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)


# views/visit.py

class VisitListView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'nimregenin/visit/visit_list.html'
    context_object_name = 'enrollment'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pre-fetch the Day 120 visit for CRF7
        context['day120_visit'] = context['enrollment'].visits.filter(
            visit_type='DAY120'
        ).first()
        return context