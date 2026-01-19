from django.urls import path
from ...views import (
    CRF6ListView,
    CRF6CreateUpdateView,
    CRF6DeleteView,
)

urlpatterns = [
    path('crf6/', CRF6ListView.as_view(), name='crf6_list'),
    path('crf6/<int:visit_pk>/new/', CRF6CreateUpdateView.as_view(), name='crf6_create'),
    path('crf6/<int:pk>/edit/', CRF6CreateUpdateView.as_view(), name='crf6_update'),
    path('crf6/<int:pk>/delete/', CRF6DeleteView.as_view(), name='crf6_delete'),
]