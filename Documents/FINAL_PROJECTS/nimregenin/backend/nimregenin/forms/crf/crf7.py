# nimregenin/forms/crf7.py (or wherever it is)

from django import forms
from django.utils import timezone
from ...models import CRF7


class CRF7Form(forms.ModelForm):
    class Meta:
        model = CRF7
        fields = [
            'visit',
            'completion_date',
            'early_termination',
            'termination_reason',
            'study_completion_status',
        ]
        widgets = {
            'completion_date': forms.DateInput(
                attrs={
                    'type': 'date',           # This enables HTML5 date picker
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DD'  # Helpful hint
                }
            ),
            'termination_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'early_termination': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'completion_date': 'Date of Study Completion/Termination',
            'early_termination': 'Early Termination',
            'termination_reason': 'Reason for Early Termination',
            'study_completion_status': 'Final Study Status',
        }
        help_texts = {
            'early_termination': 'Check if patient withdrew or was terminated before Day 120',
            'termination_reason': 'Required if early termination is checked',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make completion_date default to today if blank (optional)
        if 'completion_date' not in self.initial and not self.instance.pk:
            self.initial['completion_date'] = timezone.now().date()

        # Optional: Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name != 'visit':  # visit is usually hidden
                if not isinstance(field.widget, (forms.CheckboxInput, forms.Textarea)):
                    field.widget.attrs.update({'class': 'form-control'})