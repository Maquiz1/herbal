from django.urls import path
from ..views import (
    ScreeningListView,
    ScreeningCreateUpdateView,
    ScreeningDeleteView,
)

urlpatterns = [
    path('screening/', ScreeningListView.as_view(), name='screening_list'),
    path('screening/new/', ScreeningCreateUpdateView.as_view(), name='screening_create'),
    path('screening/<int:pk>/edit/', ScreeningCreateUpdateView.as_view(), name='screening_update'),
    path('screening/<int:pk>/delete/', ScreeningDeleteView.as_view(), name='screening_delete'),
]