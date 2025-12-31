# nimregenin/forms/screening.py

from django import forms
from django.utils import timezone
from ..models import Screening, Demographic


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
        labels = {
            'patient': 'Patient',
            'screening_date': 'Screening Date',
            'screening_status': 'Screening Status',
            'failure_reason': 'Reason for Failure',
            'screened_by': 'Screened By',
        }

    def __init__(self, *args, **kwargs):
        preselected_patient = kwargs.pop('preselected_patient', None)
        super().__init__(*args, **kwargs)

        # Base queryset: only unscreened patients
        base_qs = Demographic.objects.filter(screening__isnull=True)

        # On edit: include the current patient even if already screened
        if self.instance.pk:
            base_qs = Demographic.objects.all()  # Allow current patient

        self.fields['patient'].queryset = base_qs.select_related('site')

        # Pre-fill and hide dropdown in these cases:
        current_patient = None
        if preselected_patient:
            current_patient = preselected_patient
        elif self.instance.pk and self.instance.patient:
            current_patient = self.instance.patient

        if current_patient:
            self.initial['patient'] = current_patient
            self.initial['screening_date'] = self.initial.get('screening_date') or timezone.now().date()

            # Hide dropdown — patient cannot be changed
            self.fields['patient'].widget = forms.HiddenInput()

        # Default values on create
        if not self.instance.pk:
            self.initial.setdefault('screening_date', timezone.now().date())
            if hasattr(self, 'request'):
                self.initial.setdefault('screened_by', self.request.user)