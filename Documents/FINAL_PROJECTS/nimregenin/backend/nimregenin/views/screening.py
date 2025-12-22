"""
Screening Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .create_update import CreateUpdateView
from .delete import CRFDeleteView  # Reusable delete view
from ..models import Screening, Demographic


class ScreeningListView(LoginRequiredMixin, TemplateView):
    """
    List all screening records with patient context.
    """
    template_name = 'nimregenin/screening_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['screenings'] = (
            Screening.objects
            .select_related('patient')
            .order_by('-screening_date')
        )
        context['title'] = 'Screening Records'
        return context


class ScreeningCreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Create or Update a Screening record.
    Uses OneToOneField to Demographic (patient).
    Redirects to patient visit detail if possible, else screening list.
    """
    model = Screening
    fields = [
        'patient',           # ForeignKey to Demographic
        'screening_date',
        'screening_status',
        'failure_reason',
        'screened_by',
    ]
    template_name = 'nimregenin/screening/screening_create.html'

    def get_success_url(self):
        """
        After save, try to go back to the patient's current visit.
        Fallback: screening list.
        """
        screening = self.object
        patient = screening.patient

        # Try to find the most recent visit for this patient
        latest_visit = patient.visits.order_by('-planned_date').first()
        if latest_visit:
            return reverse_lazy(
                'nimregenin:patient_visit_detail',
                kwargs={
                    'patient_pk': patient.pk,
                    'visit_pk': latest_visit.pk
                }
            )
        return reverse_lazy('nimregenin:screening_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = f"Edit Screening - {self.object.patient.patient_id}"
        else:
            patient_id = self.request.GET.get('patient')
            patient = None
            if patient_id:
                try:
                    patient = Demographic.objects.get(pk=patient_id)
                except Demographic.DoesNotExist:
                    pass
            display = patient.patient_id if patient else "Patient"
            context['title'] = f"Add Screening - {display}"
        return context

    def get_form(self, form_class=None):
        """
        Make patient field a dropdown or pre-fill from URL.
        """
        form = super().get_form(form_class)
        # Optional: limit patient choices to those without screening yet
        form.fields['patient'].queryset = Demographic.objects.filter(screening__isnull=True)
        return form


class ScreeningDeleteView(CRFDeleteView):
    """
    Delete a screening record.
    """
    model = Screening

    def get_success_url(self):
        """
        After delete, go to patient list or last visit.
        """
        patient = self.object.patient
        latest_visit = patient.visits.order_by('-planned_date').first()
        if latest_visit:
            return reverse_lazy(
                'nimregenin:patient_visit_detail',
                kwargs={
                    'patient_pk': patient.pk,
                    'visit_pk': latest_visit.pk
                }
            )
        return reverse_lazy('nimregenin:patient_list')