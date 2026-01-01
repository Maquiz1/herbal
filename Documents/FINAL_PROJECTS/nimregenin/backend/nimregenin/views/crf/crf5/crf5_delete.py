"""
CRF5 Views: List, Create/Update, and Delete for Adverse Events
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView
from ....models import CRF5, Visit               # nimregenin.models


class CRF5DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF5 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF5