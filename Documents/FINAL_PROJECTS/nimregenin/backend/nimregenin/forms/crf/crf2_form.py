from django import forms
from django.utils import timezone
from ...models import CRF2


class CRF2Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        # Hide visit field (we show PID + Visit Day in template)
        self.fields['visit'].widget = forms.HiddenInput()

        # Pre-fill visit and visit_date if preselected_visit is provided (CREATE mode)
        if self.preselected_visit and not self.instance.pk:
            self.initial['visit'] = self.preselected_visit
            self.initial['visit_date'] = (
                getattr(self.preselected_visit, 'planned_date', None)
                or timezone.now().date()
            )

        # Default visit_date to today if creating new record
        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())

    class Meta:
        model = CRF2
        fields = [
            'visit',
            'visit_date',
            'systolic_bp',
            'diastolic_bp',
            'heart_rate',
            'temperature',
            'respiratory_rate',
            'physical_exam_findings',
            'notes',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'systolic_bp': forms.NumberInput(attrs={'class': 'form-control'}),
            'diastolic_bp': forms.NumberInput(attrs={'class': 'form-control'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'physical_exam_findings': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'visit_date': 'Date of Vital Signs',
            'systolic_bp': 'Systolic Blood Pressure (mmHg)',
            'diastolic_bp': 'Diastolic Blood Pressure (mmHg)',
            'heart_rate': 'Heart Rate (bpm)',
            'temperature': 'Temperature (°C)',
            'respiratory_rate': 'Respiratory Rate (breaths/min)',
            'physical_exam_findings': 'Physical Exam Findings',
            'notes': 'Additional Notes',
        }
        help_texts = {
            'systolic_bp': 'Measured in millimeters of mercury (mmHg)',
            'diastolic_bp': 'Measured in millimeters of mercury (mmHg)',
            'heart_rate': 'Beats per minute (bpm)',
            'temperature': 'Body temperature in degrees Celsius',
        }
