from django.urls import path
from ...views import (
    CRF2ListView,
    CRF2CreateUpdateView,
    CRF2DeleteView,
)

urlpatterns = [
    path('crf2/', CRF2ListView.as_view(), name='crf2_list'),
    path('crf2/new/', CRF2CreateUpdateView.as_view(), name='crf2_create'),
    path('crf2/<int:pk>/edit/', CRF2CreateUpdateView.as_view(), name='crf2_update'),
    path('crf2/<int:pk>/delete/', CRF2DeleteView.as_view(), name='crf2_delete'),
]