# nimregenin/forms/crf7.py

from django import forms
from django.utils import timezone
from ...models import CRF7


class CRF7Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # 🔑 Pop request out so BaseModelForm doesn’t choke
        self.request = kwargs.pop('request', None)
        self.preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        # Pre-fill visit and visit_date if preselected_visit is provided (CREATE mode)
        if self.preselected_visit:
            self.initial['visit'] = self.preselected_visit
            self.initial['visit_date'] = (
                getattr(self.preselected_visit, 'planned_date', None)
                or timezone.now().date()
            )
            # Hide the visit field since it's preselected
            self.fields['visit'].widget = forms.HiddenInput()

        # Default visit_date to today if creating new record
        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())

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
        help_texts = {
            'primary_endpoint_score': 'Score based on primary efficacy criteria.',
            'secondary_endpoint_score': 'Score based on secondary efficacy criteria.',
            'clinician_global_impression': 'Overall impression by the clinician.',
            'patient_global_impression': 'Overall impression by the patient.',
        }