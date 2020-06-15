from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from registration.views import (
    SigninView,
    SignupView,
    UserPasswordResetConfirmView,
    UserPasswordResetView,
)


class TestSignupView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user1@test.com"
        cls.password = "abcd12efgh"
        cls.signup_url = reverse("registration:signup")
        cls.client = Client()

    def test_signup_view_url_exists(self):
        response = self.client.get("/registration/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_url_accessible_by_name(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_post_blank_email(self):
        data = {"password1": self.password, "password2": self.password}
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "email", "This field is required.")

    def test_signup_view_post_blank_password1(self):
        data = {"email": self.email, "password2": self.password}
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "password1", "This field is required.")

    def test_signup_view_post_blank_passwor2(self):
        data = {"email": self.email, "password1": self.password}
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "password2", "This field is required.")

    def test_signup_view_post_blank_all(self):
        response = self.client.post(self.signup_url, {})
        self.assertFormError(response, "form", "email", "This field is required.")
        self.assertFormError(response, "form", "password1", "This field is required.")
        self.assertFormError(response, "form", "password2", "This field is required.")

    def test_signup_view_post_invalid_email(self):
        data = {
            "email": "abcdefghijk",
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_signup_view_post_invalid_passwords(self):
        data = {
            "email": self.email,
            "password1": "abcdefghij",
            "password2": "eeeeeeeee1",
        }
        response = self.client.post(self.signup_url, data)
        error = "The two password fields didn’t match."
        self.assertFormError(response, "form", "password2", error)

    def test_signup_view_success_redirect(self):
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, reverse("registration:login"))

    def test_signup_create_existing_user(self):
        get_user_model().objects.create_user(email=self.email, password=self.password)
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(self.signup_url, data)
        error = "My user with this Email already exists."
        self.assertFormError(response, "form", "email", error)

    def test_signup_create_messages(self):
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        response = self.client.post(self.signup_url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(
            message.message, "Account created successfully. You can now login"
        )


class TestSigninView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user@test.com"
        cls.password = "abcd12efgh"
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.password
        )

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
