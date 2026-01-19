# nimregenin/views/crf5.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from ...create_update_view import CreateUpdateView
from ....forms import CRF5Form
from ....models import CRF5, Enrollment


class CRF5CreateUpdateView(CreateUpdateView):
    """
    Create / Update view for CRF5 (Adverse Event Report).
    Visit dropdown is restricted to the current patient's enrollment.
    """
    model = CRF5
    form_class = CRF5Form
    template_name = 'nimregenin/crf/crf5/crf5_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_enrollment = None
        self.current_patient = None

        # 🔑 Ensure enrollment_pk is passed in URL or querystring
        enrollment_pk = kwargs.get('enrollment_pk') or request.GET.get('enrollment_pk')
        if enrollment_pk:
            self.current_enrollment = get_object_or_404(Enrollment, pk=enrollment_pk)
            self.current_patient = self.current_enrollment.patient.patient

    def get_object(self):
        obj = super().get_object()
        if obj:
            # 🔑 Restrict to the enrollment of the visit being edited
            self.current_enrollment = obj.visit.enrollment
            self.current_patient = self.current_enrollment.patient.patient
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['enrollment'] = self.current_enrollment   # 🔑 ensures dropdown is patient-specific
        return kwargs

    def get_extra_context(self):
        title_pid = self.current_patient.pid if self.current_patient else "New CRF5"
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            request=request,
            enrollment=self.current_enrollment
        )

        if form.is_valid():
            obj = form.save()
            self.object = obj
            messages.success(
                request,
                f"CRF5 adverse event reported successfully for {self.current_patient.pid}."
            )
            return redirect(self.get_success_url())

        return self.render_form(request, form)

    def get_success_url(self):
        visit = self.object.visit
        return reverse_lazy('nimregenin:visit_list', kwargs={'pk': visit.enrollment.pk})
