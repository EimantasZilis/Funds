from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from registration.views import (
    SigninView,
    SignupView,
    UserPasswordResetConfirmView,
    UserPasswordResetView,
)


class TestSigninView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user@test.com"
        cls.password = "abcd12efgh"
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.password
        )

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_signin_view_url_exists(self):
        response = self.client.get("/registration/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signin_view_url_accessible_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signin_view_post_blank_password(self):
        response = self.client.post(reverse("login"), {"username": self.email})
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_signin_view_post_blank_email(self):
        response = self.client.post(reverse("login"), {"password": self.password})
        self.assertFormError(response, "form", "username", "This field is required.")

    def test_signin_view_post_blank_email_password(self):
        response = self.client.post(reverse("login"), {})
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_signin_view_post_invalid_email(self):
        response = self.client.post(
            reverse("login"), {"username": "abcd123", "password": self.password}
        )
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(response, "form", None, error)

    def test_signin_view_post_invalid_password(self):
        response = self.client.post(
            reverse("login"), {"username": self.email, "password": "abcd"}
        )
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(response, "form", None, error)

    def test_signin_view_success_redirect(self):
        response = self.client.post(
            reverse("login"), {"username": self.email, "password": self.password}
        )
        self.assertRedirects(response, reverse("home"))

    def test_signin_view_anonymous_get(self):
        response = self.client.get(reverse("home"), follow=True)
        self.assertRedirects(response, reverse("login"))

    def test_signin_view_anonymous_post(self):
        response = self.client.post(reverse("home"), follow=True)
        self.assertRedirects(response, reverse("login"))
