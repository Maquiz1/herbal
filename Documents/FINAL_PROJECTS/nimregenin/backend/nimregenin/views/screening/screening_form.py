# nimregenin/views/screening.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from ..create_update import CreateUpdateView
from ...forms.screening import ScreeningForm
from ...models import Screening, Demographic


class ScreeningCreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    model = Screening
    form_class = ScreeningForm
    template_name = 'nimregenin/screening/screening_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.preselected_patient = None
        if not kwargs.get('pk'):  # Create mode only
            patient_id = request.GET.get('patient')
            if patient_id:
                try:
                    demographic = Demographic.objects.get(pk=patient_id)
                    # Only allow if patient has NOT been screened yet
                    if not hasattr(demographic, 'screening'):
                        self.preselected_patient = demographic
                except Demographic.DoesNotExist:
                    pass
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['preselected_patient'] = self.preselected_patient
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = None
        if self.object:
            patient = self.object.patient
            context['title'] = f"Edit Screening - {patient.pid}"
        elif self.preselected_patient:
            patient = self.preselected_patient
            context['title'] = f"Screen Patient - {patient.pid}"
        else:
            context['title'] = "Add New Screening"

        if patient:
            context['selected_patient'] = patient

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Screening for patient {form.instance.patient.pid} saved successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        # Go back to patient list after save
        return reverse_lazy('nimregenin:patient_list')