from django import forms
from ..models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'patient',
            'enrollment_date',
            'study_id',
            'randomization_number',
            'status',
            'enrolled_by',
        ]
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only patients who passed screening and not enrolled
        self.fields['patient'].queryset = Demographic.objects.filter(
            screening__screening_status='PASS',
            enrollment__isnull=True
        )