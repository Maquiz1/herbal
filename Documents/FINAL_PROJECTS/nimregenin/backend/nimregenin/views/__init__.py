from .demographic import *  # PatientListView, PatientVisitDetailView, etc.
from .screening import *
from .enrollment import *
from .visit import *
from .reminders import VoiceReminderTwiMLView
from .crf import *
from .dashboard import *
from .create_update_view import CreateUpdateView
from .export import OverduePatientsCSVExportView
from .delete import CRFDeleteView
from .protocol import TemplateDetailsView   


__all__ = [
    # dashboard views...
    'HomeView',
    
    #create_update views...
    'CreateUpdateView',
    
    # demographic views...
    'PatientListView','DemographicCreateUpdateView','PatientVisitDetailView',
    
    # screening views...
    'ScreeningListView','ScreeningDetailView','ScreeningCreateUpdateView','ScreeningDeleteView',
    
    # enrollment views...
    'EnrollmentListView','EnrollmentDetailView','EnrollmentCreateUpdateView','EnrollmentDeleteView',
    
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
