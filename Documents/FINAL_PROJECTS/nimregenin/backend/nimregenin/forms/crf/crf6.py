from django import forms
from ...models import CRF6


class CRF6Form(forms.ModelForm):
    class Meta:
        model = CRF6
        fields = [
            'visit',
            'visit_date',
            'primary_endpoint_score',
            'secondary_endpoint_score',
            'clinician_assessment',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'clinician_assessment': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'primary_endpoint_score': 'Main outcome measure (e.g., symptom score change)',
            'secondary_endpoint_score': 'Supporting measure (e.g., quality of life)',
        }