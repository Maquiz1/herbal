from django import forms
from ..models import Demographic


class DemographicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # 🔑 Pop request out of kwargs so BaseModelForm doesn’t choke
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Optional: you can use self.request for user-specific logic
        # Example: filter queryset fields based on logged-in user
        # if self.request and not self.request.user.is_superuser:
        #     self.fields['region'].queryset = (
        #         self.fields['region'].queryset.filter(user=self.request.user)
        #     )

    class Meta:
        model = Demographic
        fields = [
            'pid',
            'rec_date',
            'hid',
            'nid',
            'fname',
            'mname',
            'lname',
            'dob',
            'age',
            'gender',
            'marital_status',
            'education',
            'occupation',
            'phone_patient',
            'phone_relative',
            'region',
            'district',
            'ward',
            'street',
            'site',
            'remarks',
        ]
        labels = {
            'rec_date': 'Recruit Date',
            'pid': 'Patient ID',
            'fname': 'First Name',
            'mname': 'Middle Name',
            'lname': 'Last Name',
            'dob': 'Date of Birth',
            'age': 'Age (years)',
            'gender': 'Gender',
            'phone_patient': 'Patient Phone Number',
            'phone_relative': 'Relative/Next of Kin Phone',
            'education': 'Highest Education Level',
            'marital_status': 'Marital Status',
            'site': 'Study Site',
            'hid': 'Hospital ID',
            'nid': 'National ID',
            'remarks': 'Additional Comments',
        }
        help_texts = {
            'pid': 'Unique identifier assigned to the patient',
            'phone_patient': 'Format: +255XXXXXXXXX',
        }
        widgets = {
            'rec_date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')
        if pid and Demographic.objects.filter(pid=pid).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This PID already exists.")
        return pid
