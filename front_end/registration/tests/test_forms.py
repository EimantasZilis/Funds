from django.contrib.auth import get_user_model
from django.test import TestCase

from registration.forms import UserLoginForm, field_attrs


class FieldAttrs(TestCase):
    def test_field_attrs_default(self):
        expected_attrs = {"class": "input_form", "required": True}
        attributes = field_attrs()
        self.assertEqual(attributes, expected_attrs)

    def test_field_attrs_placeholder(self):
        placeholder = "omg"
        expected_attrs = {
            "class": "input_form",
            "required": True,
            "placeholder": placeholder,
        }
        attributes = field_attrs(placeholder=placeholder)
        self.assertEqual(attributes, expected_attrs)


class TestUserLoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "user@test.com"
        cls.password = "abcd123456"
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.password
        )

    def test_login_form_valid(self):
        data = {"username": self.user.email, "password": self.password}
        form = UserLoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_email(self):
        data = {"username": "jesus.christ@heaven.com", "password": self.password}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form_not_email(self):
        data = {"username": "not_email", "password": self.password}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form_blank_email(self):
        data = {"username": "", "password": self.password}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form_blank_password(self):
        data = {"username": self.user.email, "password": ""}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_password(self):
        data = {"username": self.email, "password": "I am Groot"}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_email_and_password(self):
        data = {"username": "jesus.christ@heaven.com", "password": "I like bagel"}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())
