# nimregenin/views/enrollment.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from ..create_update import CreateUpdateView
from ...forms.enrollment import EnrollmentForm
from ...models import Enrollment, Demographic, Screening


class EnrollmentCreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'nimregenin/enrollment/enrollment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.preselected_screening = None
        if not kwargs.get('pk'):  # Create mode only
            patient_id = request.GET.get('patient')
            if patient_id:
                try:
                    demographic = Demographic.objects.get(pk=patient_id)
                    if (hasattr(demographic, 'screening') and
                        demographic.screening.screening_status == 'PASS' and
                        not hasattr(demographic.screening, 'enrollment')):
                        self.preselected_screening = demographic.screening
                except Demographic.DoesNotExist:
                    pass
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass preselected screening for create mode
        kwargs['preselected_screening'] = self.preselected_screening
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screening = None
        if self.object:
            screening = self.object.patient
            context['title'] = f"Edit Enrollment - {screening.patient.pid}"
        elif self.preselected_screening:
            screening = self.preselected_screening
            context['title'] = f"Enroll Patient - {screening.patient.pid}"
        else:
            context['title'] = "Enroll New Patient"

        if screening:
            context['selected_patient'] = screening.patient

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Patient {form.instance.patient.patient.pid} enrollment saved successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        patient = self.object.patient.patient  # Demographic
        return reverse_lazy('nimregenin:patient_list')