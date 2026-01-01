# nimregenin/forms/crf5.py

from django import forms
from django.utils import timezone
from ...models import CRF5


class CRF5Form(forms.ModelForm):
    class Meta:
        model = CRF5
        fields = [
            'visit',
            'visit_date',
            'ae_description',
            'severity',
            'serious',
            'onset_date',
            'resolution_date',
            'outcome',
            'relationship_to_study',
            'notes',
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'onset_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resolution_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ae_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'serious': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        if preselected_visit:
            self.initial['visit'] = preselected_visit
            self.initial['visit_date'] = timezone.now().date()
            self.initial['onset_date'] = timezone.now().date()
            self.fields['visit'].widget = forms.HiddenInput()

        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())
            self.initial.setdefault('onset_date', timezone.now().date())