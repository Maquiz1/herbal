# nimregenin/forms/demographic.py

from django import forms
from django.core.exceptions import ValidationError
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
        widgets = {
            'rec_date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
            'pid': forms.TextInput(attrs={'placeholder': 'e.g., PT-001'}),
            'phone_patient': forms.TextInput(attrs={'placeholder': '+255...'}),
            'phone_relative': forms.TextInput(attrs={'placeholder': '+255...'}),
        }

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')
        if pid:
            queryset = Demographic.objects.filter(pid=pid)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError("This Patient ID (PID) already exists.")
        return pid

    def clean_nid(self):
        nid = self.cleaned_data.get('nid')
        if nid:
            queryset = Demographic.objects.filter(nid=nid)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError("This National ID already exists.")
        return nid