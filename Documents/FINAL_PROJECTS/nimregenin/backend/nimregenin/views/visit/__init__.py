from .demographic_list import PatientListView
from .demographic_detail import PatientVisitDetailView
from .demographic_form import * 
from .demographic_delete import DemographicDeleteView

__all__ = [    
    'PatientListView',
    'DemographicCreateUpdateView',
    'PatientVisitDetailView',
    'DemographicDeleteView',
]
