"""
Enrollment Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ..delete import CRFDeleteView
from ...models import Enrollment, Demographic, Visit


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

