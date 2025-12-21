from django.urls import path
from .views import (
    HomeView,
    DemographicListView, DemographicCreateUpdateView,
    ScreeningListView, ScreeningCreateUpdateView,
    EnrollmentListView, EnrollmentCreateUpdateView,
    CRF1ListView, CRF1CreateUpdateView,
    CRF2ListView, CRF2CreateUpdateView,
    CRF3ListView, CRF3CreateUpdateView,
    CRF4ListView, CRF4CreateUpdateView,
    CRF5ListView, CRF5CreateUpdateView,
    CRF6ListView, CRF6CreateUpdateView,
    CRF7ListView, CRF7CreateUpdateView,
)

app_name = 'nimregenin'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Demographic
    path('demographics/', DemographicListView.as_view(), name='demographic_list'),
    path('demographics/new/', DemographicCreateUpdateView.as_view(), name='demographic_create'),
    path('demographics/<int:pk>/edit/', DemographicCreateUpdateView.as_view(), name='demographic_update'),

    # Screening
    path('screening/', ScreeningListView.as_view(), name='screening_list'),
    path('screening/new/', ScreeningCreateUpdateView.as_view(), name='screening_create'),
    path('screening/<int:pk>/edit/', ScreeningCreateUpdateView.as_view(), name='screening_update'),

    # Enrollment
    path('enrollment/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollment/new/', EnrollmentCreateUpdateView.as_view(), name='enrollment_create'),
    path('enrollment/<int:pk>/edit/', EnrollmentCreateUpdateView.as_view(), name='enrollment_update'),

    # CRFs
    path('crf1/', CRF1ListView.as_view(), name='crf1_list'),
    path('crf1/new/', CRF1CreateUpdateView.as_view(), name='crf1_create'),
    path('crf1/<int:pk>/edit/', CRF1CreateUpdateView.as_view(), name='crf1_update'),

    # CRF2
    path('crf2/', CRF2ListView.as_view(), name='crf2_list'),
    path('crf2/new/', CRF2CreateUpdateView.as_view(), name='crf2_create'),
    path('crf2/<int:pk>/edit/', CRF2CreateUpdateView.as_view(), name='crf2_update'),

    # CRF3
    path('crf3/', CRF3ListView.as_view(), name='crf3_list'),
    path('crf3/new/', CRF3CreateUpdateView.as_view(), name='crf3_create'),
    path('crf3/<int:pk>/edit/', CRF3CreateUpdateView.as_view(), name='crf3_update'),
    
    # CRF4
    path('crf4/', CRF4ListView.as_view(), name='crf4_list'),
    path('crf4/new/', CRF4CreateUpdateView.as_view(), name='crf4_create'),
    path('crf4/<int:pk>/edit/', CRF4CreateUpdateView.as_view(), name='crf4_update'),
    
    # CRF5
    path('crf5/', CRF5ListView.as_view(), name='crf5_list'),
    path('crf5/new/', CRF5CreateUpdateView.as_view(),   name='crf5_create'),    
    path('crf5/<int:pk>/edit/', CRF5CreateUpdateView.as_view(), name='crf5_update'),
    
    # CRF6
    path('crf6/', CRF6ListView.as_view(), name='crf6_list'),
    path('crf6/new/', CRF6CreateUpdateView.as_view(), name='crf6_create'),
    path('crf6/<int:pk>/edit/', CRF6CreateUpdateView.as_view(), name='crf6_update'),
    
    # CRF7  
    path('crf7/', CRF7ListView.as_view(), name='crf7_list'),
    path('crf7/new/', CRF7CreateUpdateView.as_view(), name='crf7_create'),
    path('crf7/<int:pk>/edit/', CRF7CreateUpdateView.as_view(), name='crf7_update'),
]