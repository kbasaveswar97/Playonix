from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = [
            'company_name', 'contact_person', 'work_email', 'phone',
            'employee_count',
            'interested_annual_calendar', 'interested_tournaments',
            'interested_wellness', 'interested_custom',
            'message',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Acme Corp', 'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'}),
            'work_email': forms.EmailInput(attrs={'placeholder': 'you@company.com', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 ...', 'class': 'form-control'}),
            'employee_count': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Locations, timelines, past events, anything that helps us plan.',
                'rows': 5,
                'class': 'form-control',
            }),
        }
        labels = {
            'company_name': 'Company Name',
            'contact_person': 'Contact Person',
            'work_email': 'Work Email',
            'phone': 'Phone',
            'employee_count': 'Employee Count',
            'message': 'Anything we should know?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].required = True
        self.fields['contact_person'].required = True
        self.fields['work_email'].required = True
        self.fields['phone'].required = False
        self.fields['employee_count'].required = False
        self.fields['employee_count'].empty_label = "Select a range"
