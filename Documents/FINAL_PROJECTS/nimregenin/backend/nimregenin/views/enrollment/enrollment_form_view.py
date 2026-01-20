# nimregenin/views/enrollment.py

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ...forms import EnrollmentForm
from ...models import Enrollment, Screening


class EnrollmentCreateUpdateView(CreateUpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'nimregenin/enrollment/enrollment_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_screening = None
        self.current_patient = None

        if 'screening_pk' in kwargs:
            self.current_screening = get_object_or_404(
                Screening,
                pk=kwargs['screening_pk'],
                screening_status='PASS',
                enrollment__isnull=True
            )
            self.current_patient = self.current_screening.patient

    def get_object(self):
        obj = super().get_object()
        if obj:
            self.current_screening = obj.screening
            self.current_patient = self.current_screening.patient
        return obj

    def assign_related(self, form):
        if not self.object and self.current_screening:
            form.instance.screening = self.current_screening
        return form

    def get_extra_context(self):
        return {
            'current_screening': self.current_screening,
            'current_patient': self.current_patient,
            'title': (
                f"{'Edit' if getattr(self, 'object', None) else 'Enroll'} Patient - "
                f"{self.current_patient.pid if self.current_patient else ''}"
            )
        }

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"Patient {self.current_patient.pid} enrolled successfully."
        )
