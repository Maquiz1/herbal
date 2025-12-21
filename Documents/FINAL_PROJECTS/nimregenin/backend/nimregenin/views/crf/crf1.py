"""
CRF1 Views: List, Create/Update, and Delete for Baseline Assessment
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from decimal import Decimal, InvalidOperation, DivisionByZero
from django.shortcuts import redirect

from ..create_update import CreateUpdateView  # Base CreateUpdateView
from ..delete import CRFDeleteView              # Generic DeleteView
from ...models import CRF1   # nimregenin.models.CRF1


class CRF1ListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all CRF1 (Baseline) records.
    """
    template_name = 'nimregenin/crf1_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf1_records'] = CRF1.objects.select_related('visit__patient').order_by('-created_at')
        context['title'] = 'CRF1 - Baseline Assessment Records'
        return context


class CRF1CreateUpdateView(CreateUpdateView, LoginRequiredMixin):
    """
    Combined Create and Update view for CRF1.
    Only applicable to Baseline visits.
    Redirects to the parent visit detail page after saving.
    """
    model = CRF1
    fields = [
        'visit',
        'visit_date',
        'height_cm',
        'weight_kg',
        'bmi',
        'medical_history',
        'concomitant_medications',
    ]
    template_name = 'nimregenin/crf_form.html'


    def form_valid(self, form):
            """
            Override to calculate BMI before saving if possible.
            """
            obj = form.save(commit=False)

            height_cm = obj.height_cm
            weight_kg = obj.weight_kg

            if height_cm and weight_kg and height_cm > 0:
                try:
                    height_m = Decimal(height_cm) / 100
                    bmi = Decimal(weight_kg) / (height_m ** 2)
                    obj.bmi = round(bmi, 1)  # 1 decimal place
                except (InvalidOperation, DivisionByZero):
                    obj.bmi = None
            else:
                obj.bmi = None

            obj.save()
            self.object = obj
            return redirect(self.get_success_url())
    
    def get_success_url(self):
        """
        Redirect to the related patient's visit detail page after save.
        """
        visit = self.object.visit
        return reverse_lazy(
            'nimregenin:patient_visit_detail',
            kwargs={
                'patient_pk': visit.patient.pk,
                'visit_pk': visit.pk
            }
        )

    def get_context_data(self, **kwargs):
        """
        Add dynamic page title based on create/edit mode.
        """
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = f"Edit CRF1 - Baseline ({self.object.visit.patient.patient_id})"
        else:
            # Try to get visit from query param for better title
            visit_id = self.request.GET.get('visit')
            if visit_id:
                from ...models import Visit
                try:
                    visit = Visit.objects.get(pk=visit_id)
                    context['title'] = f"Create CRF1 - Baseline ({visit.patient.patient_id})"
                except Visit.DoesNotExist:
                    context['title'] = "Create CRF1 - Baseline Visit"
            else:
                context['title'] = "Create CRF1 - Baseline Visit"
        return context


class CRF1DeleteView(CRFDeleteView, LoginRequiredMixin):
    """
    Delete view for CRF1 records.
    Uses generic CRFDeleteView with confirmation.
    """
    model = CRF1