"""
Screening Views: List, Create/Update, and Delete
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update_view import CreateUpdateView
from ..delete import CRFDeleteView  # Reusable delete view
from ...models import Screening, Patient


class ScreeningListView(LoginRequiredMixin, TemplateView):
    """
    List all screening records with patient context.
    """
    template_name = 'nimregenin/screening/screening_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['screenings'] = (
            Screening.objects
            .select_related('patient')
            .order_by('-screening_date')
        )
        context['title'] = 'Screening Records'
        return context
