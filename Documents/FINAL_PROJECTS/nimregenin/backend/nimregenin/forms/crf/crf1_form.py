from django import forms
from ...models import CRF1


class CRF1Form(forms.ModelForm):
    # Optional: Show calculated BMI in form (read-only)
    bmi_display = forms.CharField(
        label='BMI (kg/m²)',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control bg-light'
        })
    )

    def __init__(self, *args, **kwargs):
        """
        Accept optional 'current_visit' from the view to pre-fill visit/visit_date.
        Show BMI if editing existing CRF1.
        """
        self.request = kwargs.pop('request', None)
        self.current_visit = kwargs.pop('current_visit', None)
        super().__init__(*args, **kwargs)

        # Hide visit field (we display PID + Visit Day separately in template)
        self.fields['visit'].widget = forms.HiddenInput()

        # Pre-fill visit and visit_date from current_visit (CREATE mode)
        if self.current_visit and not self.instance.pk:
            self.initial['visit'] = self.current_visit
            if hasattr(self.current_visit, 'planned_date'):
                self.initial['visit_date'] = self.current_visit.planned_date

        # Show BMI if editing existing CRF1
        if self.instance.pk and self.instance.bmi is not None:
            self.fields['bmi_display'].initial = self.instance.bmi

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

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height_cm')
        weight = cleaned_data.get('weight_kg')

        if height is not None and height <= 0:
            self.add_error('height_cm', 'Height must be greater than 0.')

        if weight is not None and weight <= 0:
            self.add_error('weight_kg', 'Weight must be greater than 0.')

        # HARD guarantee: visit must be assigned
        if not cleaned_data.get('visit') and not self.instance.visit_id:
            raise forms.ValidationError("Visit must be assigned before saving CRF1.")

        return cleaned_data
