"""
CRF2 Views: List, Create/Update, and Delete for Physical Examination
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView (already has LoginRequiredMixin)
from ...models import CRF2, Visit               # nimregenin.models


class CRF2ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF2 (Physical Examination) records.
    """
    template_name = 'nimregenin/crf/crf2/crf2_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf2_records'] = (
            CRF2.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF2 - Physical Examination Records'
        return context


class CRF2CreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Combined Create and Update view for CRF2.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF2
    fields = [
        'visit',
        'visit_date',
        'systolic_bp',
        'diastolic_bp',
        'heart_rate',
        'physical_exam_findings',
    ]
    template_name = 'nimregenin/crf/crf2/crf2_form.html'

    def get_success_url(self):
        visit = self.object.visit
        return reverse_lazy(
            'nimregenin:patient_visit_detail',
            kwargs={
                'patient_pk': visit.patient.pk,
                'visit_pk': visit.pk
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = f"Edit CRF2 - Physical Exam ({self.object.visit.get_visit_type_display()})"
        else:
            visit = None
            visit_id = self.request.GET.get('visit')
            if visit_id:
                try:
                    visit = Visit.objects.get(pk=visit_id)
                except Visit.DoesNotExist:
                    pass
            display = visit.get_visit_type_display() if visit else "Visit"
            context['title'] = f"Create CRF2 - Physical Exam ({display})"
        return context


class CRF2DeleteView(CRFDeleteView):
    """
    Delete view for CRF2 records.
    Inherits LoginRequiredMixin from CRFDeleteView — DO NOT repeat it.
    """
    model = CRF2