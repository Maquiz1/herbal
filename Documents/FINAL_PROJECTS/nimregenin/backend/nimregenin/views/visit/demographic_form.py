# nimregenin/views/patient.py or wherever you keep it

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..create_update import CreateUpdateView
from ...models import Demographic
from ...forms import DemographicForm

class DemographicCreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    model = Demographic
    form_class = DemographicForm           # ← use the form instead of fields
    template_name = 'nimregenin/demographic/demographic_form.html'

    def get_success_url(self):
        return reverse_lazy('nimregenin:patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Patient" if self.object else "Add New Patient"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.pid} saved successfully.")
        return super().form_valid(form)