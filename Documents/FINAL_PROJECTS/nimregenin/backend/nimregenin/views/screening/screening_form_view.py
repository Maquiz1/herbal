from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ...forms import ScreeningForm
from ...models import Screening, Patient


class ScreeningCreateUpdateView(CreateUpdateView):
    model = Screening
    form_class = ScreeningForm
    template_name = 'nimregenin/screening/screening_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_patient = None

        if 'patient_pk' in kwargs:
            self.current_patient = get_object_or_404(
                Patient,
                pk=kwargs['patient_pk']
            )

    def get_extra_context(self):
        patient = self.object.patient if self.object else self.current_patient
        return {
            'current_patient': patient,
            'title': (
                f"{'Edit' if self.object else 'Screen'} Patient - {patient.pid}"
                if patient else "Screen Patient"
            )
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            request=request
        )

        # 🔑 REQUIRED: assign patient BEFORE validation (CREATE)
        if not self.object:
            if not self.current_patient:
                raise ValueError("patient_pk is required for creating Screening")
            form.instance.patient = self.current_patient

        if form.is_valid():
            self.object = form.save()
            self.form_valid_success(form)
            return redirect(self.get_success_url())

        return self.render_form(request, form)

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"Screening saved for {form.instance.patient.pid}"
        )
