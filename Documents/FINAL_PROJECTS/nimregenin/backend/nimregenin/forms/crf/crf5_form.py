from django import forms
from django.utils import timezone
from ...models import CRF5, Visit


class CRF5Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.enrollment = kwargs.pop('enrollment', None)
        super().__init__(*args, **kwargs)

        if self.enrollment:
            self.fields['visit'].queryset = Visit.objects.filter(enrollment=self.enrollment).order_by('planned_date')
            self.fields['visit'].label = "Associated Visit"
            self.fields['visit'].widget = forms.Select(attrs={'class': 'form-select'})

        if not self.instance.pk:
            self.initial.setdefault('visit_date', timezone.now().date())
            self.initial.setdefault('onset_date', timezone.now().date())

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
        labels = {
            'visit_date': 'Date of Adverse Event Report',
            'ae_description': 'Adverse Event Description',
            'severity': 'Severity',
            'serious': 'Serious Adverse Event',
            'onset_date': 'Onset Date',
            'resolution_date': 'Resolution Date',
            'outcome': 'Outcome',
            'relationship_to_study': 'Relationship to Study Drug/Intervention',
            'notes': 'Additional Notes',
        }
        help_texts = {
            'serious': 'Check if the adverse event is classified as serious.',
        }
