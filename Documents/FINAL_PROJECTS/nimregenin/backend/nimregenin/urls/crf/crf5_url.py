from django.urls import path
from ...views import (
    CRF5ListView,
    CRF5CreateUpdateView,
    CRF5DeleteView,
)

urlpatterns = [
    path('crf5/', CRF5ListView.as_view(), name='crf5_list'),

    # CREATE requires enrollment_pk to filter visits to the correct patient
    path('crf5/<int:enrollment_pk>/new/', CRF5CreateUpdateView.as_view(), name='crf5_create'),

    # UPDATE and DELETE only need the CRF5 pk
    path('crf5/<int:pk>/edit/', CRF5CreateUpdateView.as_view(), name='crf5_update'),
    path('crf5/<int:pk>/delete/', CRF5DeleteView.as_view(), name='crf5_delete'),
]
