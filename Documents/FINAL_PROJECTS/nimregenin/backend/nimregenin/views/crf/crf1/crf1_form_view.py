# nimregenin/views/crf1.py

from decimal import Decimal, InvalidOperation, DivisionByZero
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404

from ...create_update_view import CreateUpdateView
from ....forms import CRF1Form
from ....models import CRF1, Visit


class CRF1CreateUpdateView(CreateUpdateView):
    """
    Create / Update view for CRF1 (Baseline Assessment).
    Only Baseline visits are allowed.
    BMI is auto-calculated.
    """
    model = CRF1
    form_class = CRF1Form
    template_name = 'nimregenin/crf/crf1/crf1_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.current_visit = None
        self.current_patient = None

        # CREATE mode: get Visit
        if 'visit_pk' in kwargs:
            self.current_visit = get_object_or_404(
                Visit,
                pk=kwargs['visit_pk'],
                visit_type='BASELINE'
            )
            self.current_patient = self.current_visit.enrollment.patient.patient

    def get_object(self):
        """
        EDIT mode: return CRF1 instance and set current_visit / current_patient
        """
        obj = super().get_object() if hasattr(super(), 'get_object') else None
        if obj:
            self.current_visit = obj.visit
            self.current_patient = obj.visit.enrollment.patient.patient
        return obj

    def get_extra_context(self):
        title_pid = (
            self.current_visit.enrollment.patient.patient.pid
            if self.current_visit else "New CRF1"
        )
        context_title = (
            f"Edit CRF1 - Baseline ({title_pid})"
            if getattr(self, 'object', None)
            else f"Add CRF1 - Baseline ({title_pid})"
        )

        return {
            'current_visit': self.current_visit,
            'current_patient': self.current_patient,
            'title': context_title,
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            current_visit=self.current_visit,  # pass to form if needed
        )

        # Bind visit for CREATE
        if not self.object:
            if not self.current_visit:
                raise ValueError("visit_pk is required to create CRF1")
            form.instance.visit = self.current_visit

        if form.is_valid():
            obj = form.save(commit=False)

            # Calculate BMI
            height_cm = obj.height_cm
            weight_kg = obj.weight_kg
            if height_cm and weight_kg and height_cm > 0:
                try:
                    height_m = Decimal(height_cm) / 100
                    bmi = Decimal(weight_kg) / (height_m ** 2)
                    obj.bmi = round(bmi, 1)
                except (InvalidOperation, DivisionByZero):
                    obj.bmi = None
            else:
                obj.bmi = None

            obj.save()
            self.object = obj

            messages.success(
                request,
                f"CRF1 saved successfully for {self.current_patient.pid}."
            )
            return redirect(self.get_success_url())

        return self.render_form(request, form)

    def get_success_url(self):
        """
        Redirect to the visit detail page (or patient list fallback)
        """
        visit = self.object.visit
        enrollment = visit.enrollment
        return reverse_lazy(
            'nimregenin:visit_list',  # adjust if you have a visit detail URL
            kwargs={'pk': enrollment.pk}
        )
