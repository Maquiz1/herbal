# nimregenin/forms/crf4.py

from django import forms
from django.utils import timezone
from ...models import CRF4


class CRF4Form(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        if preselected_visit:
            self.initial['visit'] = preselected_visit
            self.initial['visit_date'] = preselected_visit.planned_date or timezone.now().date()
            self.fields['visit'].widget = forms.HiddenInput()

        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())