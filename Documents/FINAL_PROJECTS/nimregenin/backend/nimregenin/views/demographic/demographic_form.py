# nimregenin/views/patient.py or wherever you keep it

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..create_update import CreateUpdateView
from ...models import Demographic
from ...forms import DemographicForm

class DemographicCreateUpdateView(LoginRequiredMixin, CreateUpdateView):
    """
    Create and Update view for patient demographics using the full model.
    """
    model = Demographic
    form_class = DemographicForm  # Use custom form
    template_name = 'nimregenin/demographic_form.html'  # Custom template

    def get_success_url(self):
        return reverse_lazy('nimregenin:patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = f"Edit Patient - {self.object.pid}"
        else:
            context['title'] = "Register New Patient"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.pid} saved successfully.")
        return super().form_valid(form)