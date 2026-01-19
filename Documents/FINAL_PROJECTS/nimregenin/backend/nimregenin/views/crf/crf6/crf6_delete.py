"""
CRF6 Views: List, Create/Update, and Delete for Efficacy Assessment
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update_view import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView
from ....models import CRF6, Visit               # nimregenin.models


class CRF6DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF6 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF6