from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm, PasswordResetForm

class UserCreateForm(UserCreationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Username', "class": "input_form"}),
        label=False
    )
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


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Username', "class": "input_form"}),
        label=False
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Password', "class": "input_form"}),
        label=False
    )

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