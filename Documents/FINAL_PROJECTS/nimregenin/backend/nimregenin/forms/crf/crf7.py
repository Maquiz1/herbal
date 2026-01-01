# nimregenin/forms/crf7.py

from django import forms
from django.utils import timezone
from ...models import CRF7


class CRF7Form(forms.ModelForm):
    class Meta:
        model = CRF7
        fields = [
            'visit',
            'visit_date',
            'primary_endpoint_score',
            'secondary_endpoint_score',
            'clinician_global_impression',
            'patient_global_impression',
            'clinician_assessment',
            'notes',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'clinician_assessment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'visit_date': 'Date of Efficacy Assessment',
            'primary_endpoint_score': 'Primary Endpoint Score',
            'secondary_endpoint_score': 'Secondary Endpoint Score',
            'clinician_global_impression': 'Clinician Global Impression',
            'patient_global_impression': 'Patient Global Impression',
            'clinician_assessment': 'Clinician Assessment',
            'notes': 'Additional Notes',
        }

    def __init__(self, *args, **kwargs):
        preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        if preselected_visit:
            self.initial['visit'] = preselected_visit
            self.initial['visit_date'] = preselected_visit.planned_date or timezone.now().date()
            self.fields['visit'].widget = forms.HiddenInput()

        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())