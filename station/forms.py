# parking/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(UserCreationForm):  
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')  
    last_name = forms.CharField(max_length=30, required=True, label='Nom')  
    email = forms.EmailField(max_length=254, required=True, label='Email')  
    contact_number = forms.CharField(max_length=15, required=True, label='Numéro de téléphone')  

    class Meta:  
        model = User  
        fields = ('username', 'first_name', 'last_name', 'email', 'contact_number', 'password1', 'password2')  

    def save(self, commit=True):  
        user = super().save(commit=False)  
        user.email = self.cleaned_data['email']  
        user.first_name = self.cleaned_data['first_name']  
        user.last_name = self.cleaned_data['last_name']  
        
        if commit:  
            user.save()  
            # Créer le profil associé  
            Profile.objects.create(  
                user=user,  
                first_name=self.cleaned_data['first_name'],  
                last_name=self.cleaned_data['last_name'],  
                email=self.cleaned_data['email'],  
                contact_number=self.cleaned_data['contact_number']  
            )  
        return user