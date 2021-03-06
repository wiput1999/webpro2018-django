from django import forms
from django.core.exceptions import ValidationError

from dayoff.models import Dayoff

import datetime


class DayOffForm(forms.ModelForm):
    class Meta:
        model = Dayoff
        exclude = ['approve_status', 'create_by']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        data = super().clean()

        start = data.get('date_start')
        end = data.get('date_end')


        if start > end:
            raise ValidationError('End date cannot come before start date')
        elif start < datetime.datetime.now().date():
            raise ValidationError('Please do not fill date in past')
