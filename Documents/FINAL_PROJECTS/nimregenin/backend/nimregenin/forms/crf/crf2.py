# nimregenin/forms/crf2.py

from django import forms
from django.utils import timezone
from ...models import CRF2


class CRF2Form(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        if preselected_visit:
            self.initial['visit'] = preselected_visit
            self.initial['visit_date'] = preselected_visit.planned_date or timezone.now().date()
            self.fields['visit'].widget = forms.HiddenInput()

        # Default visit_date to today if creating new
        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())