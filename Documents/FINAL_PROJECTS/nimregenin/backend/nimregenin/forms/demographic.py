from django import forms
from ..models import Demographic


class DemographicForm(forms.ModelForm):
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
            'pid': 'Patient ID',
            'fname': 'First Name',
            'lname': 'Last Name',
            'dob': 'Date of Birth',
            'age': 'Age (years)',
            'gender': 'Gender',
            'phone_patient': 'Patient Phone Number',
            'phone_relative': 'Relative/Next of Kin Phone',
            'site': 'Study Site',
            'remarks': 'Additional Comments',
        }
        help_texts = {  # Optional bonus
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