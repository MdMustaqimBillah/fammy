from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from . import models
from django.forms import DateTimeField
from django.forms.widgets import DateTimeInput



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required= True, 
                             widget=forms.TextInput(attrs={'placeholder':'Enter your email address'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password'}),
        strip=False,
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Enter your first name'}),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Enter your last name'}),
    )
    class Meta:
        model = User
        fields = ['email']
        


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
    widget=forms.TextInput(attrs={'placeholder': 'Your email'})
)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
    )
    class Meta:
        model = User
        fields = ['username']


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        required=False,
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Select gender'), ('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'select-class'})
    )
    class Meta:
        model = models.UserProfile
        fields = ['first_name','last_name','image','bio','dob','gender','location']
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'Introduce yourself'}),
            "first_name": forms.TextInput(attrs={'placeholder':'Your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder':'Your Surname'})
        }