from django import forms  # Importing Django forms
from django.contrib.auth.models import User  # Importing the User model from Django
from django.contrib.auth.forms import AuthenticationForm  # Importing Django's authentication form

# User registration form
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User  # Using Django's User model
        fields = ['username', 'email', 'password']  # Fields included in the form

# User login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

