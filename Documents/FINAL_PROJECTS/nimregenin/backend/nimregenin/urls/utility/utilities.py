from django.urls import path
from ...views import (
    HomeView,
    OverduePatientsCSVExportView,
    TemplateDetailsView,
)
from ...views.reminders import VoiceReminderTwiMLView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('export/overdue-patients/csv/', OverduePatientsCSVExportView.as_view(), name='overdue_patients_csv'),
    path('voice/reminder/', VoiceReminderTwiMLView.as_view(), name='voice_reminder'),
    path('voice/reminder/<str:site_code>/', VoiceReminderTwiMLView.as_view(), name='voice_reminder_site'),
    path('template/<str:visit_type>/', TemplateDetailsView.as_view(), name='template_details'),
    path('template/', TemplateDetailsView.as_view(), name='template_details'),
]