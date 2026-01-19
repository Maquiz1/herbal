# nimregenin/forms/crf3.py

from django import forms
from django.utils import timezone
from ...models import CRF3


class CRF3Form(forms.ModelForm):
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
        help_texts = {
            'wbc': 'White Blood Cells count',
        }
