"""
Enrollment Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ..delete import CRFDeleteView
from ...models import Enrollment, Demographic, Visit


class EnrollmentDeleteView(CRFDeleteView):
    """
    Delete an enrollment record (use with caution — breaks data integrity).
    """
    model = Enrollment

    def get_success_url(self):
        patient = self.object.patient
        return reverse_lazy('nimregenin:patient_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, f"Enrollment for {self.get_object().patient.patient_id} has been deleted.")
        return super().delete(request, *args, **kwargs)