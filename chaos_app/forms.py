from django import forms
from .models import Card

# Form for creating cards

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'content', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'maxlength': '500',
                'placeholder': 'Enter content here. Max length 500 characters.'
            }),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

