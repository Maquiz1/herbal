from .patient_list import PatientListView
from .patient_detail import PatientVisitDetailView
from .patient_form import * 
from .patient_delete import PatientDeleteView

__all__ = [    
    'PatientListView',
    'PatientCreateUpdateView',
    'PatientDeleteView',
    'PatientVisitDetailView',
]
