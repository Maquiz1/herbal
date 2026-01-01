"""
CRF7 Views: List, Create/Update, and Delete for Study Completion/Termination
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView
from ....models import CRF7, Visit               # nimregenin.models


class CRF7DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF7 records.
    Inherits LoginRequiredMixin from CRFDeleteView.
    """
    model = CRF7