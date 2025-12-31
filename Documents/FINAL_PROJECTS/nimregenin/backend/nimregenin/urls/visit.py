from django.urls import path
from ..views import (
    VisitListView,
)

urlpatterns = [
  # urls.py
path('visit/<int:pk>/', VisitListView.as_view(), name='visit_list'),
]