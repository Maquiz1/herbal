# nimregenin/views/crf/delete.py

from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404


class CRFDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Generic delete view for any CRF model.
    Redirects back to the parent visit detail page after deletion.
    """
    template_name = 'nimregenin/crf_confirm_delete.html'
    success_message = "%(model_name)s successfully deleted."

    def get_object(self, queryset=None):
        """
        Fetch the CRF instance using pk from URL.
        """
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)

    def get_success_url(self):
        """
        After deletion, go back to the visit detail page.
        """
        visit = self.object.visit
        messages.success(self.request, self.success_message % {'model_name': self.model._meta.verbose_name})
        return reverse_lazy(
            'nimregenin:patient_visit_detail',
            kwargs={
                'patient_pk': visit.patient.pk,
                'visit_pk': visit.pk
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crf_name'] = self.model._meta.verbose_name.title()
        context['visit'] = self.object.visit
        return context