# nimregenin/views/crf5.py

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ...create_update import CreateUpdateView
from ....forms import CRF5Form
from ....models import CRF5, Visit


class CRF5CreateUpdateView(CreateUpdateView,LoginRequiredMixin):
    model = CRF5
    form_class = CRF5Form
    template_name = 'nimregenin/crf/crf5/crf5_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.preselected_visit = None
        if not kwargs.get('pk'):
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
        visit = self.object.visit if self.object else self.preselected_visit
        if visit:
            context['selected_patient'] = visit.enrollment.patient.patient
            context['title'] = f"{'Edit' if self.object else 'Report'} Adverse Event ({visit.enrollment.patient.patient.pid})"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Adverse Event reported successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('nimregenin:visit_list', kwargs={'pk': self.object.visit.enrollment.pk})