# nimregenin/views/crf1.py

from decimal import Decimal, InvalidOperation, DivisionByZero
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ...create_update_view import CreateUpdateView
from ....models import CRF1, Visit
from ...create_update_view import CreateUpdateView  # Base CreateUpdateView
from ...delete import CRFDeleteView              # Generic DeleteView
from ....models import CRF1   # nimregenin.models.CRF1

class CRF1DeleteView(CRFDeleteView, LoginRequiredMixin):
    """
    Delete view for CRF1 records.
    Uses generic CRFDeleteView with confirmation.
    """
    model = CRF1