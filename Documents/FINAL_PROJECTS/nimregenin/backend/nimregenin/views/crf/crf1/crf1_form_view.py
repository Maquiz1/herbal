from decimal import Decimal, InvalidOperation, DivisionByZero
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

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

        # CREATE mode: get Visit (must be Baseline)
        visit_pk = kwargs.get('visit_pk') or request.GET.get('visit_pk')
        if visit_pk:
            self.current_visit = get_object_or_404(
                Visit,
                pk=visit_pk,
                visit_type='BASELINE'
            )
            self.current_patient = self.current_visit.enrollment.patient.patient

    def get_object(self):
        """
        EDIT mode: return CRF1 instance and set current_visit / current_patient
        """
        obj = super().get_object()
        if obj:
            self.current_visit = obj.visit
            self.current_patient = obj.visit.enrollment.patient.patient
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['current_visit'] = self.current_visit
        return kwargs

    def get_extra_context(self):
        title_pid = self.current_patient.pid if self.current_patient else "New CRF1"
        context_title = (
            f"Edit CRF1 - Baseline Assessment ({title_pid})"
            if getattr(self, 'object', None)
            else f"Add CRF1 - Baseline Assessment ({title_pid})"
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
            current_visit=self.current_visit,
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
        Redirect to the visit list for this enrollment
        """
        visit = self.object.visit
        enrollment = visit.enrollment
        return reverse_lazy(
            'nimregenin:visit_list',
            kwargs={'pk': enrollment.pk}
        )
