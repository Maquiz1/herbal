from django.urls import path
from ..views import (
    PatientListView,
    PatientCreateUpdateView,
    PatientVisitDetailView,
)

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/new/', PatientCreateUpdateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', PatientCreateUpdateView.as_view(), name='patient_update'),
    path('patients/<int:patient_pk>/visit/<int:visit_pk>/', PatientVisitDetailView.as_view(), name='patient_visit_detail'),
]