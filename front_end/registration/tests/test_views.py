from django.contrib.auth import get_user_model
from django.test import TestCase
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

    def test_signin_view_url_exists(self):
        response = self.client.get("/registration/login/")
        self.assertEqual(response.status_code, 200)

    def test_signin_view_url_accessible_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_signin_view_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
