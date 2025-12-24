from django import forms
from ...models import CRF3


class CRF3Form(forms.ModelForm):
    class Meta:
        model = CRF3
        fields = [
            'visit',
            'visit_date',
            'height_cm',
            'weight_kg',
            'medical_history',
            'concomitant_medications',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 4}),
            'concomitant_medications': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height_cm')
        weight = cleaned_data.get('weight_kg')

        if height and weight and height > 0:
            from decimal import Decimal
            bmi = Decimal(weight) / ((Decimal(height) / 100) ** 2)
            cleaned_data['bmi'] = round(bmi, 1)
        return cleaned_data