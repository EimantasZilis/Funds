from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView

from registration import forms as registration_forms


class SignupView(SuccessMessageMixin, CreateView):
    form_class = registration_forms.UserCreateForm
    success_url = reverse_lazy("registration:login")
    template_name = "registration/signup.html"
    success_message = "Account created successfully. You can now login"


class SigninView(LoginView):
    form_class = registration_forms.UserLoginForm
    template_name = "registration/login.html"


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = registration_forms.UserPasswordResetForm
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy("registration:login")
    success_message = mark_safe(
        "We’ve emailed you instructions for resetting your password.<br>"
        "If you don’t receive an email, make sure you’ve entered "
        "the correct email and check your spam folder."
    )


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = registration_forms.UserPasswordResetConfirmForm
    success_url = reverse_lazy("registration:login")
    template_name = "registration/password_reset_confirm.html"
    success_message = mark_safe("Your password has been reset. You can login now.")
