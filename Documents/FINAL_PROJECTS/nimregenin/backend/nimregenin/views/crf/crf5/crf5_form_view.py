from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from ...create_update_view import CreateUpdateView
from ....forms import CRF5Form
from ....models import CRF5, Enrollment


class CRF5CreateUpdateView(CreateUpdateView):
    model = CRF5
    form_class = CRF5Form
    template_name = 'nimregenin/crf/crf5/crf5_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_enrollment = None
        self.current_patient = None

        # Accept enrollment_pk from URL or querystring
        enrollment_pk = kwargs.get('enrollment_pk') or request.GET.get('enrollment_pk')
        if enrollment_pk:
            self.current_enrollment = get_object_or_404(Enrollment, pk=enrollment_pk)
            # 🔑 Enrollment → Screening → Patient
            self.current_patient = self.current_enrollment.screening.patient

    def get_object(self):
        obj = super().get_object()
        if obj:
            self.current_enrollment = obj.visit.enrollment
            self.current_patient = self.current_enrollment.screening.patient
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['current_enrollment'] = self.current_enrollment   # pass enrollment into form
        return kwargs

    def get_extra_context(self):
        title_pid = getattr(self.current_patient, "pid", None) or "New CRF5"
        context_title = (
            f"Edit CRF5 - Adverse Event ({title_pid})"
            if getattr(self, 'object', None)
            else f"Report CRF5 - Adverse Event ({title_pid})"
        )
        return {
            'current_enrollment': self.current_enrollment,
            'current_patient': self.current_patient,
            'title': context_title,
        }

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"CRF5 adverse event reported successfully for {getattr(self.current_patient, 'pid', 'Unknown PID')}."
        )

    def get_success_url(self):
        visit = self.object.visit
        return reverse_lazy('nimregenin:visit_list', kwargs={'pk': visit.enrollment.pk})
