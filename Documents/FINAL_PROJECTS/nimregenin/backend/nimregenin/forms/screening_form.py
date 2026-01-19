from django import forms
from django.utils import timezone
from ..models import Screening


class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = [
            'screening_date',
            'screening_status',
            'failure_reason',
            'screened_by',
        ]
        widgets = {
            'screening_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'failure_reason': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Patient is NEVER handled by the form.
        It must be assigned by the view BEFORE validation.
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Defaults for CREATE only
        if not self.instance.pk:
            self.initial.setdefault(
                'screening_date',
                timezone.now().date()
            )
            if self.request and self.request.user.is_authenticated:
                self.initial.setdefault(
                    'screened_by',
                    self.request.user
                )

    def clean(self):
        cleaned_data = super().clean()

        # Hard guarantee: patient must already be assigned
        if not self.instance.patient_id:
            raise forms.ValidationError(
                "Patient must be assigned before saving Screening."
            )

        return cleaned_data
