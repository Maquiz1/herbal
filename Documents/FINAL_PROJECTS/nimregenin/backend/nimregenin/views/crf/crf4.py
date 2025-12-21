"""
CRF4 Views: List, Create/Update, and Delete for Concomitant Medications Update
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView
from ...models import CRF4, Visit               # nimregenin.models


class CRF4ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF4 (Concomitant Medications) records.
    """
    template_name = 'nimregenin/crf4_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf4_records'] = (
            CRF4.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF4 - Concomitant Medications Records'
        return context


class CRF4CreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Combined Create and Update view for CRF4.
    Used to track ongoing concomitant medications at each visit.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF4
    fields = [
        'visit',
        'visit_date',
        'medication_name',
        'dose',
        'start_date',
        'end_date',
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
                f"Edit CRF4 - Con Meds ({self.object.visit.get_visit_type_display()})"
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
            context['title'] = f"Create CRF4 - Con Meds ({display})"
        return context


class CRF4DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF4 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF4