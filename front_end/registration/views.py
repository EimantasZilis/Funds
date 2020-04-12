from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from registration import forms as registration_forms

class SignupView(CreateView):
    form_class = registration_forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class SigninView(LoginView):
    form_class = registration_forms.UserLoginForm
    template_name = "registration/login.html"

