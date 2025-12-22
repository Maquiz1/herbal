from .demographic import *  # PatientListView, PatientVisitDetailView, etc.
from .reminders import VoiceReminderTwiMLView
from .crf import *
from .dashboard import HomeView
from .create_update import CreateUpdateView
from .export import OverduePatientsCSVExportView
from .delete import CRFDeleteView
from .screening import ScreeningListView, ScreeningCreateUpdateView, ScreeningDeleteView
from .enrollment import EnrollmentListView, EnrollmentCreateUpdateView
from .protocol import TemplateDetailsView   


__all__ = [
    # dashboard views...
    'HomeView',
    
    #create_update views...
    'CreateUpdateView',
    
    # demographic views...
    'PatientListView','DemographicCreateUpdateView','PatientVisitDetailView',
    
    # screening views...
    'ScreeningListView','ScreeningCreateUpdateView','ScreeningDeleteView',
    
    # enrollment views...
    'EnrollmentListView','EnrollmentCreateUpdateView',
    
    # protocol views...
    'TemplateDetailsView',
    
    # export views...
    'OverduePatientsCSVExportView', 
    
    # patient views...
    'VoiceReminderTwiMLView',
    
    # crf views...
    'CRF1CreateUpdateView',
    'CRF2CreateUpdateView',
    'CRF3CreateUpdateView',
    'CRF4CreateUpdateView',
    'CRF5CreateUpdateView',
    'CRF6CreateUpdateView',
    'CRF7CreateUpdateView',
    
    
    'CRFDeleteView',
]
