from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    redirect_field_name = None
