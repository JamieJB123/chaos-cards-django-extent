from django import forms
from .models import CollaborateRequest

# Feedback / collaborate form

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CollaborateRequest
        fields = ('name', 'email', 'message',)
        widgets = {
            'name': forms.TextInput(attrs={
                'maxlength': '200',
                'placeholder': 'Your Name',
            }),
            'email': forms.EmailInput(attrs={
                'maxlength': '254',
                'placeholder': 'Your Email'
            }),
            'message': forms.Textarea(attrs={
                'maxlength': '500',
                'placeholder': 'Your Message'
            })
        }
