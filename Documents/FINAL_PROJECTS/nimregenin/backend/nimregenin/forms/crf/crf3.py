from django import forms
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
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'hemoglobin': 'g/dL',
            'wbc': '×10³/μL',
            'platelets': '×10³/μL',
            'creatinine': 'mg/dL',
            'alt': 'U/L (SGPT)',
            'ast': 'U/L (SGOT)',
        }