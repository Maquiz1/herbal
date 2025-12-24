from django import forms
from ...models import CRF7


class CRF7Form(forms.ModelForm):
    class Meta:
        model = CRF7
        fields = [
            'visit',
            'completion_date',
            'early_termination',
            'termination_reason',
            'study_completion_status',
        ]
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_reason': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'early_termination': 'Check if patient withdrew before study end',
            'termination_reason': 'Required if early termination',
        }