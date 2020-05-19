from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.safestring import mark_safe

from registration import forms as registration_forms

class SignupView(SuccessMessageMixin, CreateView):
    form_class = registration_forms.UserCreateForm
    success_url = reverse_lazy('registration:login')
    template_name = 'registration/signup.html'
    success_message = "Account created successfully. You can now login"

class SigninView(LoginView):
    form_class = registration_forms.UserLoginForm
    template_name = "registration/login.html"

class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = registration_forms.UserPasswordResetForm
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy('registration:login')
    success_message = mark_safe(
        "We’ve emailed you instructions for resetting your password. "
        "You should receive them shortly.<br>"
        "If you don’t receive an email, please make sure you’ve entered "
        "the correct email and check your spam folder."
    )

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = registration_forms.UserPasswordResetConfirmForm
    success_url = reverse_lazy('registration:login')
    template_name = 'registration/password_reset_confirm.html'
    success_message = "Your password has been reset. You can login now."