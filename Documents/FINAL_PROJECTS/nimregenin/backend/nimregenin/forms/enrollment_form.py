from django import forms
from django.core.exceptions import ValidationError
from ..models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['enrollment_date', 'study_id', 'randomization_number', 'status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # 🔑 Ensure uniqueness: one Enrollment per Screening
        if self.instance and self.instance.screening:
            qs = Enrollment.objects.filter(screening=self.instance.screening)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    f"Patient {self.instance.screening.patient.pid} already has an enrollment record."
                )

        return cleaned_data
