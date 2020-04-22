from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView

from registration import forms as registration_forms

class SignupView(CreateView):
    form_class = registration_forms.UserCreateForm
    success_url = reverse_lazy('registration:signup_completed')
    template_name = 'registration/signup.html'

class SigninView(LoginView):
    form_class = registration_forms.UserLoginForm
    template_name = "registration/login.html"

class SignupCompletedView(TemplateView):
    template_name = "registration/signup_completed.html"

class UserPasswordResetView(PasswordResetView):
    form_class = registration_forms.UserPasswordResetForm
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy('password_reset_done')

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = registration_forms.UserPasswordResetConfirmForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'