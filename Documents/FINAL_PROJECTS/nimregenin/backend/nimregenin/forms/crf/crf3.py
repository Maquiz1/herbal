# nimregenin/forms/crf3.py

from django import forms
from django.utils import timezone
from ...models import CRF3


class CRF3Form(forms.ModelForm):
    class Meta:
        model = CRF3
        fields = [
            'visit',
            'visit_date',
            'hemoglobin',
            'wbc',
            'platelets',
            'creatinine',
            'alt',
            'ast',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hemoglobin': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'wbc': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'platelets': forms.NumberInput(attrs={'class': 'form-control'}),
            'creatinine': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'alt': forms.NumberInput(attrs={'class': 'form-control'}),
            'ast': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'visit_date': 'Date of Lab Test',
            'hemoglobin': 'Hemoglobin (g/dL)',
            'wbc': 'White Blood Cells (×10³/µL)',
            'platelets': 'Platelets (×10³/µL)',
            'creatinine': 'Creatinine (mg/dL)',
            'alt': 'ALT (U/L)',
            'ast': 'AST (U/L)',
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