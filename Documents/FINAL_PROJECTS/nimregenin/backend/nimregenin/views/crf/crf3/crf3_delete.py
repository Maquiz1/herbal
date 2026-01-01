"""
CRF3 Views: List, Create/Update, and Delete for Laboratory Results
"""

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ...create_update import CreateUpdateView  # Base CreateUpdateView in views/
from ...delete import CRFDeleteView              # Generic DeleteView in crf/
from ....models import CRF3, Visit               # nimregenin.models


class CRF3DeleteView(CRFDeleteView,LoginRequiredMixin):
    """
    Delete view for CRF3 records.
    Inherits LoginRequiredMixin from CRFDeleteView — DO NOT repeat.
    """
    model = CRF3