from django import forms
from .models import PhoneBook

class PhoneBookForm(forms.ModelForm):
    class Meta:
        model = PhoneBook
        fields = ['name', 'phone_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
