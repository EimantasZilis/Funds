from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
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

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = registration_forms.UserPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_message = "Your password has been changed"
    success_url = reverse_lazy("home")

class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = registration_forms.UserPasswordResetConfirmForm
    success_url = reverse_lazy("registration:login")
    template_name = "registration/password_reset_confirm.html"
    success_message = mark_safe("Your password has been reset")
    error_message = mark_safe("Password reset link is not valid")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """
        Redirect back to the login page with a warning
        if the password reset link is invalid.
        """

        dispatch_return = super().dispatch(*args, **kwargs)

        token = kwargs["token"]
        valid_token = self.token_generator.check_token(self.user, token)
        if valid_token or token == self.reset_url_token:
            return dispatch_return
        else:
            messages.add_message(self.request, messages.ERROR, self.error_message)
            return HttpResponseRedirect(reverse_lazy("registration:login"))
