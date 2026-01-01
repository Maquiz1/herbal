# nimregenin/forms/crf1.py

from django import forms
from ...models import CRF1


class CRF1Form(forms.ModelForm):
    class Meta:
        model = CRF1
        fields = [
            'visit',
            'visit_date',
            'height_cm',
            'weight_kg',
            'medical_history',
            'concomitant_medications',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'height_cm': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'weight_kg': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'concomitant_medications': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'visit_date': 'Visit Date',
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',
            'medical_history': 'Medical History',
            'concomitant_medications': 'Concomitant Medications',
        }

    # Optional: Show calculated BMI in form (read-only)
    bmi_display = forms.CharField(
        label='BMI (kg/m²)',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control bg-light'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show current BMI if editing
        if self.instance.pk and self.instance.bmi:
            self.fields['bmi_display'].initial = self.instance.bmi

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height_cm')
        weight = cleaned_data.get('weight_kg')

        if height and weight:
            if height <= 0:
                self.add_error('height_cm', 'Height must be greater than 0.')
            # No need to set bmi here — model.save() handles it
        return cleaned_data