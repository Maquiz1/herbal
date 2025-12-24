"""
CRF7 Views: List, Create/Update, and Delete for Study Completion/Termination
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView
from ...models import CRF7, Visit               # nimregenin.models


class CRF7ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF7 (Study Completion/Termination) records.
    Typically only at final visit or early termination.
    """
    template_name = 'nimregenin/crf/crf7/crf7_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf7_records'] = (
            CRF7.objects
            .select_related('visit__patient')
            .order_by('-created_at')
        )
        context['title'] = 'CRF7 - Study Completion/Termination Records'
        return context


class CRF7CreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Combined Create and Update view for CRF7.
    Usually only for Day 120 or early withdrawal.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF7
    fields = [
        'visit',
        'completion_date',
        'early_termination',
        'termination_reason',
        'study_completion_status',
    ]
    template_name = 'nimregenin/crf/crf7/crf7_form.html'

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
                f"Edit CRF7 - Completion ({self.object.visit.get_visit_type_display()})"
            )
        else:
            visit = None
            visit_id = self.request.GET.get('visit')
            if visit_id:
                try:
                    visit = Visit.objects.get(pk=visit_id)
                except Visit.DoesNotExist:
                    pass
            display = visit.get_visit_type_display() if visit else "Final Visit"
            context['title'] = f"Create CRF7 - Completion ({display})"
        return context


class CRF7DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF7 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF7