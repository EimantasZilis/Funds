from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm
)
from django.forms.widgets import EmailInput, PasswordInput, TextInput 

from .models import MyUser

class UserCreateForm(UserCreationForm):
    email = forms.CharField(
        widget=EmailInput(attrs={'placeholder':'Email', "class": "input_form"}),
        label=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "input_form"}),
        label=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation', "class": "input_form"}),
        label=False
    )
    class Meta:
        model = MyUser
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=EmailInput(attrs={'placeholder':'Email', "class": "input_form"}),
        label=False
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Password', "class": "input_form"}),
        label=False
    )
    class Meta:
        model = MyUser
        fields = ('username', 'password')
        

class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        widget=EmailInput(attrs={'placeholder':'Email', "class": "input_form"}),
        label=False
    )

class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "input_form"}),
        label=False
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation', "class": "input_form"}),
        label=False
    )