from django.urls import path
from ...views import (
    CRF7ListView,
    CRF7CreateUpdateView,
    CRF7DeleteView,
)

urlpatterns = [
    path('crf7/', CRF7ListView.as_view(), name='crf7_list'),
    path('crf7/new/', CRF7CreateUpdateView.as_view(), name='crf7_create'),
    path('crf7/<int:pk>/edit/', CRF7CreateUpdateView.as_view(), name='crf7_update'),
    path('crf7/<int:pk>/delete/', CRF7DeleteView.as_view(), name='crf7_delete'),
]