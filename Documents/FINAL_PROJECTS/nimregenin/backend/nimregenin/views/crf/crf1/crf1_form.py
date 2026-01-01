# nimregenin/views/crf1.py

from decimal import Decimal, InvalidOperation, DivisionByZero
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse

from ...create_update import CreateUpdateView
from ....models import CRF1, Visit


class CRF1CreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    """
    Create/Update view for CRF1 (Baseline Assessment).
    Only for Baseline visits.
    BMI is auto-calculated.
    """
    model = CRF1
    fields = [
        'visit',
        'visit_date',
        'height_cm',
        'weight_kg',
        'medical_history',
        'concomitant_medications',
    ]  # bmi removed — editable=False
    template_name = 'nimregenin/crf/crf1/crf1_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.preselected_visit = None
        if not kwargs.get('pk'):  # Create mode
            visit_id = request.GET.get('visit')
            if visit_id:
                self.preselected_visit = get_object_or_404(Visit, pk=visit_id, visit_type='BASELINE')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.preselected_visit:
            initial['visit'] = self.preselected_visit
            initial['visit_date'] = self.preselected_visit.planned_date
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['preselected_visit'] = self.preselected_visit
        return kwargs

    def form_valid(self, form):
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

        messages.success(self.request, "CRF1 - Baseline Assessment saved successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Redirect to the visit detail page (or patient list fallback)
        """
        visit = self.object.visit
        enrollment = visit.enrollment
        return reverse_lazy(
            'nimregenin:visit_list',  # or your visit detail URL
            kwargs={'pk': enrollment.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        visit = None
        if self.object:
            visit = self.object.visit
            title_pid = visit.enrollment.patient.patient.pid
            context['title'] = f"Edit CRF1 - Baseline ({title_pid})"
        elif self.preselected_visit:
            visit = self.preselected_visit
            title_pid = visit.enrollment.patient.patient.pid
            context['title'] = f"Add CRF1 - Baseline ({title_pid})"
        else:
            context['title'] = "Add CRF1 - Baseline Assessment"

        if visit:
            context['selected_patient'] = visit.enrollment.patient.patient
            context['selected_visit'] = visit

        return context