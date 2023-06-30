from django import forms
from .models import Appointment



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'nurse', 'appoint_date',
                  'appoint_time', 'treatment']

        widgets = {
            'appoint_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'appoint_time': forms.TimeInput(attrs={'type': 'time', 'class': 'input'}),
            'doctor': forms.Select(attrs={'class': 'input'}),
            'nurse': forms.Select(attrs={'class': 'input'}),
            'treatment': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
        }
