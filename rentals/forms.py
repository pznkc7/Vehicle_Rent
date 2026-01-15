from django import forms
from django.contrib.auth.models import User
from .models import Rental_User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', 'Passwords do not match')


class RentalUserForm(forms.ModelForm):
    class Meta:
        model = Rental_User
        exclude = ['user']
       

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'temporary_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

