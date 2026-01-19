"""
CRF2 Views: List, Create/Update, and Delete for Physical Examination
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update_view import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView (already has LoginRequiredMixin)
from ....models import CRF2, Visit               # nimregenin.models


class CRF2DeleteView(CRFDeleteView):
    """
    Delete view for CRF2 records.
    Inherits LoginRequiredMixin from CRFDeleteView — DO NOT repeat it.
    """
    model = CRF2