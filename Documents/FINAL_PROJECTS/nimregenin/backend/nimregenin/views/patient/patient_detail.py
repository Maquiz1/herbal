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
    Patient, Visit, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)

class PatientVisitDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a specific patient visit showing all CRFs.
    """
    model = Visit
    template_name = 'nimregenin/patient_visit_detail.html'
    context_object_name = 'visit'
    pk_url_kwarg = 'visit_pk'

    def get_queryset(self):
        return Visit.objects.select_related('patient').prefetch_related(
            'crf1', 'crf2', 'crf3', 'crf4', 'crf5', 'crf6', 'crf7'
        )

    def get_object(self, queryset=None):
        patient_pk = self.kwargs.get('patient_pk')
        visit_pk = self.kwargs.get('visit_pk')
        return get_object_or_404(Visit, patient__pk=patient_pk, pk=visit_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = self.object
        patient = visit.patient
        context['patient'] = patient

        # CRF configuration
        crfs = {
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

        # Pre-compute safe URLs to avoid template reverse errors
        from django.urls import reverse
        for crf in crfs.values():
            if crf['instance']:
                crf['update_url_safe'] = reverse(crf['update_url'], args=[crf['instance'].pk])
                crf['delete_url_safe'] = reverse(crf['delete_url'], args=[crf['instance'].pk])
            else:
                crf['update_url_safe'] = None
                crf['delete_url_safe'] = None

        context['crfs'] = crfs

        # CRF completion count
        completed = sum(1 for c in crfs.values() if c['exists'])
        expected = 6
        if visit.visit_type == 'BASELINE':
            expected += 1
        if visit.visit_type == 'DAY120':
            expected += 1
        context['crf_completion'] = f"{completed}/{expected}"

        return context
