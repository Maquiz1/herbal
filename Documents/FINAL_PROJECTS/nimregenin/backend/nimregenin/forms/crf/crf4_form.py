# nimregenin/forms/crf4.py

from django import forms
from django.utils import timezone
from ...models import CRF4


class CRF4Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        # Hide visit field (we show PID + Visit Day in template)
        self.fields['visit'].widget = forms.HiddenInput()

        # Pre-fill visit and visit_date if preselected_visit is provided (CREATE mode)
        if self.preselected_visit and not self.instance.pk:
            self.initial['visit'] = self.preselected_visit
            self.initial['visit_date'] = (
                getattr(self.preselected_visit, 'planned_date', None)
                or timezone.now().date()
            )

        # Default visit_date to today if creating new record
        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())

    class Meta:
        model = CRF4
        fields = [
            'visit',
            'visit_date',
            'no_conmeds',
            'medications',
            'notes',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medications': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'no_conmeds': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'visit_date': 'Date of Concomitant Medications',
            'no_conmeds': 'No Concomitant Medications',
            'medications': 'Medications',
            'notes': 'Additional Notes',
        }
        help_texts = {
            'no_conmeds': 'Check if the patient is not taking any concomitant medications.',
        }
