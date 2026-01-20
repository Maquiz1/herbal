# nimregenin/views/patient.py

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ...models import Patient
from ...forms import PatientForm


class PatientCreateUpdateView(CreateUpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'nimregenin/patient/patient_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def get_extra_context(self):
        return {
            'title': "Edit Patient" if self.object else "Add New Patient"
        }

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"Patient {form.instance.pid} saved successfully."
        )
