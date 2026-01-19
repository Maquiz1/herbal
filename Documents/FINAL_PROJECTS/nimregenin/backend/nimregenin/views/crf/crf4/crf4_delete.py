"""
CRF4 Views: List, Create/Update, and Delete for Concomitant Medications Update
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update_view import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView
from ....models import CRF4, Visit               # nimregenin.models


class CRF4DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF4 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF4