from django.urls import path
from ...views import (
    CRF5ListView,
    CRF5CreateUpdateView,
    CRF5DeleteView,
)

urlpatterns = [
    path('crf5/', CRF5ListView.as_view(), name='crf5_list'),
    path('crf5/new/', CRF5CreateUpdateView.as_view(), name='crf5_create'),
    path('crf5/<int:pk>/edit/', CRF5CreateUpdateView.as_view(), name='crf5_update'),
    path('crf5/<int:pk>/delete/', CRF5DeleteView.as_view(), name='crf5_delete'),
]