# nimregenin/forms/__init__.py

from .demographic import DemographicForm
from .screening import ScreeningForm
from .enrollment import EnrollmentForm
from .crf.crf1 import CRF1Form
from .crf.crf2 import CRF2Form
from .crf.crf3 import CRF3Form
from .crf.crf4 import CRF4Form
from .crf.crf5 import CRF5Form
from .crf.crf6 import CRF6Form
from .crf.crf7 import CRF7Form

__all__ = [
    'DemographicForm',
    'ScreeningForm',
    'EnrollmentForm',
    'CRF1Form', 'CRF2Form', 'CRF3Form',
    'CRF4Form', 'CRF5Form', 'CRF6Form', 'CRF7Form',
]