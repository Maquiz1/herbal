"""
CRF6 Views: List, Create/Update, and Delete for Efficacy Assessment
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView
from ...models import CRF6, Visit               # nimregenin.models


class CRF6ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF6 (Efficacy Assessment) records.
    """
    template_name = 'nimregenin/crf/crf6/crf6_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf6_records'] = (
            CRF6.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF6 - Efficacy Assessment Records'
        return context


class CRF6CreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    """
    Combined Create and Update view for CRF6.
    Records efficacy endpoints at each visit.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF6
    fields = [
        'visit',
        'visit_date',
        'primary_endpoint_score',
        'secondary_endpoint_score',
        'clinician_assessment',
    ]
    template_name = 'nimregenin/crf/crf6/crf6_form.html'

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
        Add dynamic page title based on create/edit mode.
        """
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = (
                f"Edit CRF6 - Efficacy ({self.object.visit.get_visit_type_display()})"
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
            context['title'] = f"Create CRF6 - Efficacy ({display})"
        return context


class CRF6DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF6 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF6