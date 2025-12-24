"""
Enrollment Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

from .create_update import CreateUpdateView
from .delete import CRFDeleteView
from ..models import Enrollment, Demographic, Visit


class EnrollmentListView(LoginRequiredMixin, TemplateView):
    """
    List all enrollment records with patient context.
    """
    template_name = 'nimregenin/enrollment/enrollment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = (
            Enrollment.objects
            .select_related('patient')
            .order_by('-enrollment_date')
        )
        context['title'] = 'Enrollment Records'
        return context


class EnrollmentCreateUpdateView(CreateUpdateView,LoginRequiredMixin, ):
    """
    Create or Update an Enrollment record.
    OneToOne with Demographic.
    """
    model = Enrollment
    fields = [
        'patient',
        'enrollment_date',
        'study_id',
        'randomization_number',
        'status',
        'enrolled_by',
    ]
    template_name = 'nimregenin/crf_form.html'

    def get_success_url(self):
        """
        After save, go to the patient's baseline visit if it exists.
        Fallback: patient list.
        """
        enrollment = self.object
        patient = enrollment.patient

        # Find baseline visit (Day 0)
        baseline_visit = patient.visits.filter(visit_type='BASELINE').first()
        if baseline_visit:
            return reverse_lazy(
                'nimregenin:patient_visit_detail',
                kwargs={
                    'patient_pk': patient.pk,
                    'visit_pk': baseline_visit.pk
                }
            )
        return reverse_lazy('nimregenin:patient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['title'] = f"Edit Enrollment - {self.object.patient.patient_id}"
        else:
            patient_id = self.request.GET.get('patient')
            patient = None
            if patient_id:
                try:
                    patient = Demographic.objects.get(pk=patient_id)
                except Demographic.DoesNotExist:
                    pass
            display = patient.patient_id if patient else "Patient"
            context['title'] = f"Enroll Patient - {display}"
        return context

    def get_form(self, form_class=None):
        """
        Limit patient choices to those who are screened but not yet enrolled.
        """
        form = super().get_form(form_class)
        form.fields['patient'].queryset = Demographic.objects.filter(
            screening__screening_status='PASS',
            enrollment__isnull=True
        )
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.patient.patient_id} successfully enrolled.")
        return super().form_valid(form)


class EnrollmentDeleteView(CRFDeleteView):
    """
    Delete an enrollment record (use with caution — breaks data integrity).
    """
    model = Enrollment

    def get_success_url(self):
        patient = self.object.patient
        return reverse_lazy('nimregenin:patient_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, f"Enrollment for {self.get_object().patient.patient_id} has been deleted.")
        return super().delete(request, *args, **kwargs)