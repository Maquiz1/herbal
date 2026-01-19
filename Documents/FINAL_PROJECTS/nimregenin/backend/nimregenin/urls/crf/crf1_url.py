from django.urls import path
from ...views import (
    CRF1ListView,
    CRF1CreateUpdateView,
    CRF1DeleteView,
)

urlpatterns = [
    path('crf1/', CRF1ListView.as_view(), name='crf1_list'),
    path('crf1/<int:visit_pk>/new/', CRF1CreateUpdateView.as_view(), name='crf1_create'),
    path('crf1/<int:pk>/edit/', CRF1CreateUpdateView.as_view(), name='crf1_update'),
    path('crf1/<int:pk>/delete/', CRF1DeleteView.as_view(), name='crf1_delete'),
]