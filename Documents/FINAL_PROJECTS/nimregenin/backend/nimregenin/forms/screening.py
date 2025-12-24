from django import forms
from ..models import Screening


class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = [
            'patient',
            'screening_date',
            'screening_status',
            'failure_reason',
            'screened_by',
        ]
        widgets = {
            'screening_date': forms.DateInput(attrs={'type': 'date'}),
            'failure_reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit patient choices to those without screening
        self.fields['patient'].queryset = Demographic.objects.filter(screening__isnull=True)