from django.urls import path
from ...views import (
    CRF3ListView,
    CRF3CreateUpdateView,
    CRF3DeleteView,
)

urlpatterns = [
    path('crf3/', CRF3ListView.as_view(), name='crf3_list'),
    path('crf3/new/', CRF3CreateUpdateView.as_view(), name='crf3_create'),
    path('crf3/<int:pk>/edit/', CRF3CreateUpdateView.as_view(), name='crf3_update'),
    path('crf3/<int:pk>/delete/', CRF3DeleteView.as_view(), name='crf3_delete'),
]