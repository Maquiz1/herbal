from django import forms
from django.utils import timezone
from ...models import CRF6, Visit


class CRF6Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.enrollment = kwargs.pop('enrollment', None)
        super().__init__(*args, **kwargs)

        if self.enrollment:
            self.fields['visit'].queryset = Visit.objects.filter(enrollment=self.enrollment).order_by('planned_date')
            self.fields['visit'].label = "Completion Visit"
            self.fields['visit'].widget = forms.Select(attrs={'class': 'form-select'})

        if not self.instance.pk:
            self.initial.setdefault('completion_date', timezone.now().date())

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

    def clean(self):
        cleaned_data = super().clean()
        early_termination = cleaned_data.get('early_termination')
        termination_reason = cleaned_data.get('termination_reason')
        other_reason = cleaned_data.get('other_reason')
        visit = cleaned_data.get('visit')

        if early_termination and not termination_reason:
            self.add_error('termination_reason', 'This field is required for early termination.')

        if termination_reason == 'OTHER' and not other_reason:
            self.add_error('other_reason', 'Please specify the reason when "Other" is selected.')

        if visit and not self.instance.pk:
            enrollment = visit.enrollment
            if CRF6.objects.filter(visit__enrollment=enrollment).exists():
                raise forms.ValidationError(
                    "A CRF6 record already exists for this patient/enrollment. "
                    "Only one completion/termination form is allowed."
                )

        return cleaned_data
