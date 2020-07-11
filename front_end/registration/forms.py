from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.validators import EmailValidator
from django.forms.widgets import EmailInput, PasswordInput, TextInput

from .models import User


def field_attrs(placeholder=None):
    """
    Generate field attributes:
     - class: 'input_form'
     - sets 'required' flag
    Optional placeholder cam also be given.
    """
    attributes = {"class": "input_form", "required": True}
    if placeholder is not None:
        attributes["placeholder"] = placeholder
    return attributes


class UserCreateForm(UserCreationForm):
    email = forms.CharField(widget=EmailInput(attrs=field_attrs("Email")))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("Password"))
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("Password confirmation"))
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs=field_attrs("Email")), validators=[EmailValidator],
    )
    password = forms.CharField(widget=PasswordInput(attrs=field_attrs("Password")))

    class Meta:
        model = User
        fields = ("username", "password")


class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        widget=TextInput(attrs=field_attrs("Email")), validators=[EmailValidator],
    )


class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("Password"))
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("Password confirmation"))
    )

class UserPasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("Current password"))
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("New password"))
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=field_attrs("New password confirmation"))
    )