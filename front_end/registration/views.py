from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from registration import forms


class SignupView(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LoggedOutView(TemplateView):
    template_name = "registration/logout.html"

class LoggedInView(TemplateView):
    template_name = "registration/logged_in.html"
