from django.urls import path
from ...views import (
    CRF4ListView,
    CRF4CreateUpdateView,
    CRF4DeleteView,
)

urlpatterns = [
    path('crf4/', CRF4ListView.as_view(), name='crf4_list'),
    path('crf4/<int:visit_pk>/new/', CRF4CreateUpdateView.as_view(), name='crf4_create'),
    path('crf4/<int:pk>/edit/', CRF4CreateUpdateView.as_view(), name='crf4_update'),
    path('crf4/<int:pk>/delete/', CRF4DeleteView.as_view(), name='crf4_delete'),
]