from django import forms
from ...models import CRF2


class CRF2Form(forms.ModelForm):
    class Meta:
        model = CRF2
        fields = [
            'visit',
            'visit_date',
            'systolic_bp',
            'diastolic_bp',
            'heart_rate',
            'physical_exam_findings',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'physical_exam_findings': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'systolic_bp': 'Systolic blood pressure in mmHg',
            'diastolic_bp': 'Diastolic blood pressure in mmHg',
            'heart_rate': 'Heart rate in beats per minute',
            'physical_exam_findings': 'Summary of physical examination (e.g., "Normal", "Mild edema")',
        }

    def clean(self):
        cleaned_data = super().clean()
        systolic = cleaned_data.get('systolic_bp')
        diastolic = cleaned_data.get('diastolic_bp')

        if systolic and diastolic and systolic <= diastolic:
            raise forms.ValidationError("Systolic BP must be greater than diastolic BP.")
        return cleaned_data