"""
Screening Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update_view import CreateUpdateView
from ..delete import CRFDeleteView  # Reusable delete view
from ...models import Screening, Demographic


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