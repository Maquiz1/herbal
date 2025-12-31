# nimregenin/forms/enrollment.py

from django import forms
from django.utils import timezone
from ..models import Enrollment, Screening


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'patient',  # Screening object
            'enrollment_date',
            'study_id',
            'randomization_number',
            'status',
            'enrolled_by',
        ]
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'patient': 'Screened Patient',
            'enrollment_date': 'Enrollment Date',
            'study_id': 'Study ID',
            'randomization_number': 'Randomization Number',
            'status': 'Status',
            'enrolled_by': 'Enrolled By',
        }

    def __init__(self, *args, **kwargs):
        preselected_screening = kwargs.pop('preselected_screening', None)
        super().__init__(*args, **kwargs)

        # Base queryset: only PASS screened and not enrolled
        base_qs = Screening.objects.filter(
            screening_status='PASS',
            enrollment__isnull=True
        ).select_related('patient')

        # On edit: include the current screening even if already enrolled
        if self.instance.pk:
            base_qs = Screening.objects.all()

        self.fields['patient'].queryset = base_qs

        # Determine current screening (from preselect or instance)
        current_screening = None
        if preselected_screening:
            current_screening = preselected_screening
        elif self.instance.pk and self.instance.patient:
            current_screening = self.instance.patient

        if current_screening:
            self.initial['patient'] = current_screening

            # Hide dropdown — patient cannot be changed
            self.fields['patient'].widget = forms.HiddenInput()

        # Default date to today on create
        if not self.instance.pk:
            self.initial.setdefault('enrollment_date', timezone.now().date())
            if hasattr(self, 'request'):
                self.initial.setdefault('enrolled_by', self.request.user)