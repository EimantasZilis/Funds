from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.shortcuts import resolve_url
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from registration.views import (
    SigninView,
    SignupView,
    UserPasswordChangeView,
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
        cls.valid_data = {
            "email": cls.email,
            "password1": cls.password,
            "password2": cls.password,
        }

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
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertRedirects(response, reverse("registration:login"))

    def test_signup_create_existing_user(self):
        get_user_model().objects.create_user(email=self.email, password=self.password)
        response = self.client.post(self.signup_url, self.valid_data)
        error = "My user with this Email already exists."
        self.assertFormError(response, "form", "email", error)

    def test_signup_create_messages(self):
        response = self.client.post(self.signup_url, self.valid_data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, SignupView.success_message)


class TestSigninView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user@test.com"
        cls.password = "abcd12efgh"
        cls.client = Client()
        cls.valid_data = {"username": cls.email, "password": cls.password}
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
        data = {"username": "abcd123", "password": self.password}
        response = self.client.post(reverse("login"), data)
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(response, "form", None, error)

    def test_signin_view_post_invalid_password(self):
        data = {"username": self.email, "password": "abcd"}
        response = self.client.post(reverse("login"), data)
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(response, "form", None, error)

    def test_signin_view_success_redirect(self):
        response = self.client.post(reverse("login"), self.valid_data)
        self.assertRedirects(response, reverse("home"))

    def test_signin_view_anonymous_get(self):
        response = self.client.get(reverse("home"), follow=True)
        self.assertRedirects(response, reverse("login"))

    def test_signin_view_anonymous_post(self):
        response = self.client.post(reverse("home"), follow=True)
        self.assertRedirects(response, reverse("login"))


class TestSignupView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user1@test.com"
        cls.password = "abcd12efgh"
        cls.signup_url = reverse("registration:signup")
        cls.client = Client()
        cls.valid_data = {
            "email": cls.email,
            "password1": cls.password,
            "password2": cls.password,
        }

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
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertRedirects(response, reverse("registration:login"))

    def test_signup_create_existing_user(self):
        get_user_model().objects.create_user(email=self.email, password=self.password)
        response = self.client.post(self.signup_url, self.valid_data)
        error = "User with this Email already exists."
        self.assertFormError(response, "form", "email", error)

    def test_signup_success_message(self):
        response = self.client.post(self.signup_url, self.valid_data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, SignupView.success_message)


class TestUserPasswordResetView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user@test.com"
        cls.password = "abcd12efgh"
        cls.client = Client()
        cls.view_url = reverse("registration:reset_password")
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.password
        )

    def test_password_reset_view_url_exists(self):
        response = self.client.get("/registration/reset_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_form.html")

    def test_password_reset_view_url_accessible_by_name(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_form.html")

    def test_password_reset_view_post_blank_email(self):
        response = self.client.post(self.view_url, {"email": ""})
        self.assertFormError(response, "form", "email", "This field is required.")

    def test_password_reset_view_post_invalid_email(self):
        # This is a weird one. It still accepts invalid
        # password with incorrect email. EmailValidator
        # isn't working for some reason?
        response = self.client.post(self.view_url, {"email": "abvd"}, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, UserPasswordResetView.success_message)

    def test_password_reset_view_post_valid_email(self):
        response = self.client.post(self.view_url, {"email": self.email}, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, UserPasswordResetView.success_message)

    def test_password_reset_view_success_redirect(self):
        response = self.client.post(self.view_url, {"email": self.email})
        self.assertRedirects(response, reverse("login"))

    def test_password_reset_view_send_email(self):
        response = self.client.post(self.view_url, {"email": self.email})
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_view_non_existing_user_redirect(self):
        response = self.client.post(
            self.view_url, {"email": f"non-existing-{self.email}"}
        )
        self.assertRedirects(response, reverse("login"))

    def test_password_reset_view_non_existing_user_success_message(self):
        response = self.client.post(
            self.view_url, {"email": f"non-existing-{self.email}"}, follow=True
        )
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, UserPasswordResetView.success_message)

    def test_password_reset_view_non_existing_user_dont_send_email(self):
        response = self.client.post(
            self.view_url, {"email": f"non-existing-{self.email}"}, follow=True
        )
        self.assertEqual(len(mail.outbox), 0)

class TestUserPasswordChangeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user@test.com"
        cls.old_password = "abcd12efgh"
        cls.new_password = "efghi56789"
        cls.client = Client()
        cls.view_url = reverse("registration:change_password")
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.old_password
        )

    def test_password_change_view_url_exists(self):
        self.client.login(username=self.email, password=self.old_password)
        response = self.client.get("/registration/change_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_change_form.html")

    def test_password_change_view_url_accessible_by_name(self):
        self.client.login(username=self.email, password=self.old_password)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_change_form.html")

    def test_password_change_view_redirect_unauthenticated_users(self):
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": self.new_password}
        response = self.client.get(self.view_url, follow=True)
        self.assertRedirects(response, "/registration/login/?next=/registration/change_password/")

    def test_password_change_view_post_blank_old_password(self):
        self.client.login(username=self.email, password=self.old_password)
        data = { "old_password": "", "new_password1": self.new_password, "new_password2": self.new_password}
        response = self.client.post(self.view_url, data)
        self.assertFormError(response, "form", "old_password", "This field is required.")

    def test_password_change_view_post_blank_new_password1(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": "", "new_password2": self.new_password}
        response = self.client.post(self.view_url, data)
        self.assertFormError(response, "form", "new_password1", "This field is required.")

    def test_password_change_view_post_blank_new_password2(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": ""}
        response = self.client.post(self.view_url, data)
        self.assertFormError(response, "form", "new_password2", "This field is required.")

    def test_password_change_view_post_invalid_old_password(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": "111111111", "new_password1": self.new_password, "new_password2": self.new_password}
        response = self.client.post(self.view_url, data, follow=True)
        error = "Your old password was entered incorrectly. Please enter it again."
        self.assertFormError(response, "form", "old_password", error)

    def test_password_change_view_post_different_new_passwords(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": "11111eeee122"}
        response = self.client.post(self.view_url, data, follow=True)
        error = "The two password fields didn’t match."
        self.assertFormError(response, "form", "new_password2", error)

    def test_password_change_view_post_success_url(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": self.new_password}
        response = self.client.post(self.view_url, data, follow=True)

        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, UserPasswordChangeView.success_message)

    def test_password_change_view_success_redirect(self):
        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": self.new_password}
        response = self.client.post(self.view_url, data, follow=True)
        self.assertRedirects(response, reverse("home"))

    def test_password_change_view_confirm_new_credentials(self):
        # Try to login with new (incorrect) password
        incorrect_login_client = Client()
        login_data = {"username": self.email, "password": self.new_password}
        login_response = incorrect_login_client.post(reverse("login"), login_data)
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(login_response, "form", None, error)

        self.client.login(username=self.email, password=self.old_password)
        data = {"old_password": self.old_password, "new_password1": self.new_password, "new_password2": self.new_password}
        password_change_response = self.client.post(self.view_url, data, follow=True)
        self.assertRedirects(password_change_response, reverse("home"))

        # Try to login
        login_client = Client()
        login_response = login_client.post(reverse("login"), login_data)
        self.assertRedirects(login_response, reverse("home"))

class TestUserPasswordResetConfirmView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test_user1@test.com"
        cls.psw = "abcd12efgh"
        cls.new_psw = "temptemp1234"
        cls.valid_data = {"new_password1": cls.new_psw, "new_password2": cls.new_psw}

        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.psw
        )
        cls.user_b64 = urlsafe_base64_encode(force_bytes(cls.user.pk))

        token_generator = PasswordResetTokenGenerator()
        cls.token = token_generator.make_token(cls.user)

        cls.get_view_url = resolve_url(
            "password_reset_confirm", cls.user_b64, cls.token
        )
        cls.post_view_url = f"/registration/reset/{cls.user_b64}/set-password/"

    def _init_session_token(self):
        self.client.get(self.post_view_url)
        session = self.client.session
        session["_password_reset_token"] = self.token
        session.save()

    def _invalid_user_base64(self):
        last_char = self.user_b64[:-1]
        new_char = "y" if last_char == "x" else "x"
        return f"{self.user_b64[:-1]}{new_char}"

    def _invalid_user_token(self):
        last_char = self.token[:-1]
        new_char = "y" if last_char == "x" else "x"
        return f"{self.token[:-1]}{new_char}"

    def test_password_reset_confirm_view_url_exists(self):
        response = self.client.get(self.get_view_url)
        self.assertRedirects(response, self.post_view_url)

    def test_password_reset_view_url_accessible_by_name(self):
        response = self.client.get(self.get_view_url)
        self.assertRedirects(response, self.post_view_url)

    def test_password_reset_confirm_view_template(self):
        response = self.client.get(self.get_view_url, follow=True)
        self.assertTemplateUsed(response, "registration/password_reset_confirm.html")

    def test_password_reset_confirm_view_success_confirm_new_credentials(self):
        # Try to login with new (incorrect) password
        login_client = Client()
        login_data = {"username": self.email, "password": self.new_psw}
        login_response = login_client.post(reverse("login"), login_data)
        error = (
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive."
        )
        self.assertFormError(login_response, "form", None, error)

        # Reset password
        self._init_session_token()
        password_reset_response = self.client.post(self.post_view_url, self.valid_data)
        self.assertRedirects(password_reset_response, reverse("login"))

        # Try to login
        login_client = Client()
        login_response = login_client.post(reverse("login"), login_data)
        self.assertRedirects(login_response, reverse("home"))

    def test_password_reset_confirm_view_success_message(self):
        self._init_session_token()
        response = self.client.post(self.post_view_url, self.valid_data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-success")
        self.assertEqual(message.message, UserPasswordResetConfirmView.success_message)

    def test_password_reset_confirm_view_blank_password1(self):
        self._init_session_token()
        data = {"new_password1": "", "new_password2": self.new_psw}
        response = self.client.post(self.post_view_url, data)
        self.assertFormError(
            response, "form", "new_password1", "This field is required."
        )

    def test_password_reset_confirm_view_blank_password2(self):
        self._init_session_token()
        data = {"new_password1": self.new_psw, "new_password2": ""}
        response = self.client.post(self.post_view_url, data)
        self.assertFormError(
            response, "form", "new_password2", "This field is required."
        )

    def test_password_reset_confirm_view_blank_all(self):
        self._init_session_token()
        data = {"new_password1": "", "new_password2": ""}
        response = self.client.post(self.post_view_url, data)
        self.assertFormError(
            response, "form", "new_password1", "This field is required."
        )
        self.assertFormError(
            response, "form", "new_password2", "This field is required."
        )

    def test_password_reset_confirm_view_post_invalid_passwords(self):
        self._init_session_token()
        data = {"new_password1": "abcdefghij", "new_password2": "eeeeeeeee1"}
        response = self.client.post(self.post_view_url, data)
        error = "The two password fields didn’t match."
        self.assertFormError(response, "form", "new_password2", error)

    def test_password_reset_confirm_view_short_passwords(self):
        self._init_session_token()
        data = {"new_password1": "a", "new_password2": "a"}
        response = self.client.post(self.post_view_url, data)
        error = [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common.",
        ]
        self.assertFormError(response, "form", "new_password2", error)

    def test_password_reset_confirm_view_invalid_user_get_redirected(self):
        invalid_u64 = self._invalid_user_base64()
        url = resolve_url("password_reset_confirm", invalid_u64, self.token)
        response = self.client.get(url)
        self.assertRedirects(response, reverse("registration:login"))

    def test_password_reset_confirm_view_invalid_token_get_redirected(self):
        invalid_token = self._invalid_user_token()
        url = resolve_url("password_reset_confirm", self.user_b64, invalid_token)
        response = self.client.get(url)
        self.assertRedirects(response, reverse("registration:login"))

    def test_password_reset_confirm_view_invalid_user_redirect_get_message(self):
        invalid_u64 = self._invalid_user_base64()
        url = resolve_url("password_reset_confirm", invalid_u64, self.token)

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-danger")
        self.assertEqual(message.message, UserPasswordResetConfirmView.error_message)

    def test_password_reset_confirm_view_invalid_token_get_message(self):
        invalid_token = self._invalid_user_token()
        url = resolve_url("password_reset_confirm", self.user_b64, invalid_token)

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "alert-danger")
        self.assertEqual(message.message, UserPasswordResetConfirmView.error_message)
