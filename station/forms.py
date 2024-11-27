# parking/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

'''
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, help_text='Votre prénom')
    last_name = forms.CharField(max_length=100, required=True, help_text='Votre nom de famille')
    email = forms.EmailField(required=True, help_text='Votre adresse e-mail')
    contact_number = forms.CharField(max_length=15, required=True, help_text='Votre numéro de contact')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'contact_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                contact_number=self.cleaned_data['contact_number']
            )
            profile.save()
        return user

'''
 
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
