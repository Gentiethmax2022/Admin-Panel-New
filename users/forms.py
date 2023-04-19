from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.utils import timezone

from users.models import MyUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")
    date_of_birth = forms.DateField(help_text="Required. Enter your date of  birth.")
    
    class Meta:
        model = MyUser
        fields = ('email', 'date_of_birth', 'password1', 'password2')
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} is already in use")

        date_of_birth = cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth >= timezone.now().date() - timezone.timedelta(days=365*18):
            raise forms.ValidationError("You must be at least 18 years old to register")
        return cleaned_data
        
    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     try:
    #         user = MyUser.objects.filter(email=email)
    #     except Exception as e:
    #         return email
    #     raise forms.ValidationError(f"Email {email} is already in use")
    
    
    # def clean_date_of_birth(self):
    #     date_of_birth = self.cleaned_data.get('date_of_birth')
    #     if date_of_birth and date_of_birth >= timezone.now().date() - timezone.timedelta(days=365*18):
    #         raise forms.ValidationError("You must be at least 18 years old to register")
    #     return date_of_birth
    


            
            
    