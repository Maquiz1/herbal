from django import forms
from ...models import CRF5


class CRF5Form(forms.ModelForm):
    class Meta:
        model = CRF5
        fields = [
            'visit',
            'visit_date',
            'medication_name',
            'dose',
            'start_date',
            'end_date',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'dose': 'e.g., 81mg daily, 500mg BID',
            'end_date': 'Leave blank if ongoing',
        }