from django import forms
from herbal.models import Subject


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "subject_id",
            "site",
            "first_name",
            "last_name",
            "sex",
            "date_of_birth",
        ]
