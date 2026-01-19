from django.urls import path
from ..views import (
    EnrollmentListView,
    EnrollmentCreateUpdateView,
    EnrollmentDeleteView,
)

urlpatterns = [
    path('enrollment/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollment/<int:screening_pk>/new/', EnrollmentCreateUpdateView.as_view(), name='enrollment_create'),
    path('enrollment/<int:pk>/edit/', EnrollmentCreateUpdateView.as_view(), name='enrollment_update'),
    path('enrollment/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]