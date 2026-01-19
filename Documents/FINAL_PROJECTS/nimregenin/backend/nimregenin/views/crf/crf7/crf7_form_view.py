# nimregenin/views/crf7.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from ...create_update_view import CreateUpdateView
from ....forms import CRF7Form
from ....models import CRF7, Visit


class CRF7CreateUpdateView(CreateUpdateView):
    """
    Create / Update view for CRF7 (Efficacy Assessment).
    Visit is preselected and hidden in the form.
    """
    model = CRF7
    form_class = CRF7Form
    template_name = 'nimregenin/crf/crf7/crf7_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_visit = None
        self.current_patient = None

        # CREATE mode: get Visit
        visit_pk = kwargs.get('visit_pk') or request.GET.get('visit_pk')
        if visit_pk:
            self.current_visit = get_object_or_404(Visit, pk=visit_pk)
            self.current_patient = self.current_visit.enrollment.patient.patient

    def get_object(self):
        obj = super().get_object()
        if obj:
            self.current_visit = obj.visit
            self.current_patient = obj.visit.enrollment.patient.patient
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['preselected_visit'] = self.current_visit
        return kwargs

    def get_extra_context(self):
        title_pid = self.current_patient.pid if self.current_patient else "New CRF7"
        context_title = (
            f"Edit CRF7 - Efficacy Assessment ({title_pid})"
            if getattr(self, 'object', None)
            else f"Add CRF7 - Efficacy Assessment ({title_pid})"
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
            request=request,
            preselected_visit=self.current_visit
        )

        # Bind visit for CREATE
        if not self.object:
            if not self.current_visit:
                raise ValueError("visit_pk is required to create CRF7")
            form.instance.visit = self.current_visit

        if form.is_valid():
            obj = form.save()
            self.object = obj

            messages.success(
                request,
                f"CRF7 saved successfully for {self.current_patient.pid}."
            )
            return redirect(self.get_success_url())

        return self.render_form(request, form)

    def get_success_url(self):
        visit = self.object.visit
        enrollment = visit.enrollment
        return reverse_lazy(
            'nimregenin:visit_list',
            kwargs={'pk': enrollment.pk}
        )
