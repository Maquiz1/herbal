from django.shortcuts import get_object_or_404, redirect
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

        # CREATE mode: get Screening
        if 'screening_pk' in kwargs:
            self.current_screening = get_object_or_404(
                Screening,
                pk=kwargs['screening_pk'],
                screening_status='PASS',
                enrollment__isnull=True
            )
            self.current_patient = self.current_screening.patient

    def get_object(self):
        """
        For EDIT mode: return Enrollment instance and set screening/patient
        """
        obj = super().get_object() if hasattr(super(), 'get_object') else None
        if obj:
            self.current_screening = obj.screening
            self.current_patient = self.current_screening.patient

        return obj

    def get_extra_context(self):
        return {
            'current_screening': self.current_screening,
            'current_patient': self.current_patient,
            'title': (
                f"{'Edit' if getattr(self, 'object', None) else 'Enroll'} Patient - "
                f"{self.current_patient.pid if self.current_patient else ''}"
            )
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            request=request
        )

        # bind screening for CREATE
        if not self.object:
            if not self.current_screening:
                raise ValueError("screening_pk is required to create Enrollment")
            form.instance.screening = self.current_screening

        if form.is_valid():
            self.object = form.save()
            messages.success(
                request,
                f"Patient {self.current_patient.pid} enrolled successfully."
            )
            return redirect(self.get_success_url())

        return self.render_form(request, form)
