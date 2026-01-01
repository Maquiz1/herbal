# nimregenin/views/crf2.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ...create_update import CreateUpdateView
from ....forms import CRF2Form
from ....models import CRF2, Visit


class CRF2CreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    model = CRF2
    form_class = CRF2Form
    template_name = 'nimregenin/crf/crf2/crf2_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.preselected_visit = None
        if not kwargs.get('pk'):  # Create mode
            visit_id = request.GET.get('visit')
            if visit_id:
                self.preselected_visit = get_object_or_404(Visit, pk=visit_id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['preselected_visit'] = self.preselected_visit
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = None
        if self.object:
            visit = self.object.visit
            pid = visit.enrollment.patient.patient.pid
            context['title'] = f"Edit CRF2 - Vital Signs ({pid})"
        elif self.preselected_visit:
            visit = self.preselected_visit
            pid = visit.enrollment.patient.patient.pid
            context['title'] = f"Add CRF2 - Vital Signs ({pid})"
        else:
            context['title'] = "Add CRF2 - Vital Signs"

        if visit:
            context['selected_patient'] = visit.enrollment.patient.patient
            context['selected_visit'] = visit

        return context

    def form_valid(self, form):
        messages.success(self.request, "CRF2 - Vital Signs saved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        visit = self.object.visit
        enrollment = visit.enrollment
        return reverse_lazy('nimregenin:visit_list', kwargs={'pk': enrollment.pk})