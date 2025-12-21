"""
CRF5 Views: List, Create/Update, and Delete for Adverse Events
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView
from ...models import CRF5, Visit               # nimregenin.models


class CRF5ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF5 (Adverse Events) records.
    """
    template_name = 'nimregenin/crf5_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf5_records'] = (
            CRF5.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF5 - Adverse Events Records'
        return context


class CRF5CreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    """
    Combined Create and Update view for CRF5.
    Used to record adverse events at each visit.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF5
    fields = [
        'visit',
        'visit_date',
        'ae_description',
        'severity',
        'serious',
        'outcome',
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
        Add dynamic page title based on create/edit mode.
        """
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = (
                f"Edit CRF5 - Adverse Event ({self.object.visit.get_visit_type_display()})"
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
            context['title'] = f"Create CRF5 - Adverse Event ({display})"
        return context


class CRF5DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF5 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF5