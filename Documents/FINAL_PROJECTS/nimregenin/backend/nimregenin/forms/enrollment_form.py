# nimregenin/forms/enrollment.py

from django import forms
from django.utils import timezone
from ..models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'enrollment_date',
            'study_id',
            'randomization_number',
            'status',
            'enrolled_by',
        ]
        widgets = {
            'enrollment_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Screening (FK: patient) is NEVER handled by the form.
        It must be assigned by the view BEFORE validation.
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Defaults for CREATE only
        if not self.instance.pk:
            self.initial.setdefault(
                'enrollment_date',
                timezone.now().date()
            )
            if self.request and self.request.user.is_authenticated:
                self.initial.setdefault(
                    'enrolled_by',
                    self.request.user
                )

    def clean(self):
        cleaned_data = super().clean()

        # HARD guarantee: Enrollment must already be bound to Screening
        if not self.instance.patient_id:
            raise forms.ValidationError(
                "Screening must be assigned before saving Enrollment."
            )

        return cleaned_data
