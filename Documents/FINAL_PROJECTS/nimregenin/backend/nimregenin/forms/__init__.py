# nimregenin/forms/__init__.py

from .demographic_form import DemographicForm
from .screening_form import ScreeningForm
from .enrollment_form import EnrollmentForm
from .crf.crf1_form import CRF1Form
from .crf.crf2_form import CRF2Form
from .crf.crf3_form import CRF3Form
from .crf.crf4_form import CRF4Form
from .crf.crf5_form import CRF5Form
from .crf.crf6_form import CRF6Form
from .crf.crf7_form import CRF7Form

__all__ = [
    'DemographicForm',
    'ScreeningForm',
    'EnrollmentForm',
    'CRF1Form', 'CRF2Form', 'CRF3Form',
    'CRF4Form', 'CRF5Form', 'CRF6Form', 'CRF7Form',
]