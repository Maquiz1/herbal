from django import forms
from ...models import CRF4


class CRF4Form(forms.ModelForm):
    class Meta:
        model = CRF4
        fields = [
            'visit',
            'visit_date',
            'ae_description',
            'severity',
            'serious',
            'outcome',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'ae_description': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'serious': 'Check if SAE (death, life-threatening, hospitalization, etc.)',
        }