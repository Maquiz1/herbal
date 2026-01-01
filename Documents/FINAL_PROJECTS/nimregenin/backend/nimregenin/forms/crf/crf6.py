# nimregenin/forms/crf6.py

from django import forms
from django.utils import timezone
from ...models import CRF6


class CRF6Form(forms.ModelForm):
    class Meta:
        model = CRF6
        fields = [
            'visit',
            'completion_date',
            'early_termination',
            'termination_reason',
            'other_reason',
            'study_completion_status',
            'final_notes',
        ]
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'other_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'final_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'early_termination': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'completion_date': 'Date of Completion/Termination',
            'early_termination': 'Early Termination',
            'termination_reason': 'Reason for Termination',
            'other_reason': 'Other Reason (if applicable)',
            'study_completion_status': 'Final Study Status',
            'final_notes': 'Final Notes',
        }

    def __init__(self, *args, **kwargs):
        preselected_visit = kwargs.pop('preselected_visit', None)
        super().__init__(*args, **kwargs)

        if preselected_visit:
            self.initial['visit'] = preselected_visit
            self.initial['completion_date'] = preselected_visit.planned_date or timezone.now().date()
            self.fields['visit'].widget = forms.HiddenInput()

        if not self.instance.pk:
            self.initial.setdefault('completion_date', timezone.now().date())

    def clean(self):
        cleaned_data = super().clean()
        early_termination = cleaned_data.get('early_termination')
        termination_reason = cleaned_data.get('termination_reason')
        other_reason = cleaned_data.get('other_reason')

        if early_termination and not termination_reason:
            self.add_error('termination_reason', 'This field is required for early termination.')

        if termination_reason == 'OTHER' and not other_reason:
            self.add_error('other_reason', 'Please specify the reason when "Other" is selected.')

        return cleaned_data