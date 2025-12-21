"""
CRF3 Views: List, Create/Update, and Delete for Laboratory Results
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView in views/
from ..delete import CRFDeleteView              # Generic DeleteView in crf/
from ...models import CRF3, Visit               # nimregenin.models


class CRF3ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF3 (Laboratory Results) records.
    """
    template_name = 'nimregenin/crf3_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf3_records'] = (
            CRF3.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF3 - Laboratory Results Records'
        return context


class CRF3CreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Combined Create and Update view for CRF3.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF3
    fields = [
        'visit',
        'visit_date',
        'hemoglobin',
        'wbc',
        'platelets',
        'creatinine',
        'alt',
        'ast',
    ]
    template_name = 'nimregenin/crf_form.html'

    def get_success_url(self):
        """
        Redirect to the related visit detail page after save.
        """
        visit = self.object.visit
        return reverse_lazy(
            'nimregenin:patient_visit_detail',
            kwargs={
                'patient_pk': visit.patient.pk,
                'visit_pk': visit.pk
            }
        )

    def get_context_data(self, **kwargs):
        """
        Add dynamic title based on mode and visit.
        """
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = (
                f"Edit CRF3 - Labs ({self.object.visit.get_visit_type_display()})"
            )
        else:
            visit = None
            visit_id = self.request.GET.get('visit')
            if visit_id:
                try:
                    visit = Visit.objects.get(pk=visit_id)
                except Visit.DoesNotExist:
                    pass
            display = visit.get_visit_type_display() if visit else "Visit"
            context['title'] = f"Create CRF3 - Labs ({display})"
        return context


class CRF3DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF3 records.
    Inherits LoginRequiredMixin from CRFDeleteView — DO NOT repeat.
    """
    model = CRF3