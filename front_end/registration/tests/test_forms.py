from django.contrib.auth import get_user_model
from django.test import TestCase

from registration.forms import (
    UserCreateForm,
    UserLoginForm,
    UserPasswordChangeForm,
    UserPasswordResetConfirmForm,
    UserPasswordResetForm,
    field_attrs,
)


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


class TestUserCreateForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "user1@test.com"
        cls.password = "abcd123456efg"

    def test_create_valid_user(self):
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        form = UserCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_create_user_short_passwords(self):
        data = {
            "email": self.email,
            "password1": self.password[:4],
            "password2": self.password[:4],
        }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_different_passwords(self):
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": f"{self.password}_big",
        }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_first_blank_password(self):
        data = {"email": self.email, "password1": "", "password2": self.password}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_second_blank_password(self):
        data = {"email": self.email, "password1": self.password, "password2": ""}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_blank_passwords(self):
        data = {"email": self.email, "password1": "", "password2": ""}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_blank_email(self):
        data = {"email": "", "password1": self.password, "password2": self.password}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_user_all_blank(self):
        data = {"email": "", "password1": "", "password2": ""}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_crete_user_not_email(self):
        data = {"email": "abde", "password1": self.password, "password2": self.password}
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())


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

    def test_login_form_blank_email_and_password(self):
        data = {"username": "", "password": ""}
        form = UserLoginForm(data=data)
        self.assertFalse(form.is_valid())


class TestUserPasswordResetForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "user@test.com"
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password="abcd123456"
        )

    def test_valid_email(self):
        data = {"email": self.email}
        form = UserPasswordResetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        data = {"email": "111@abc.com"}
        form = UserPasswordResetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_email(self):
        data = {"email": ""}
        form = UserPasswordResetForm(data=data)
        self.assertFalse(form.is_valid())

class TestUserPasswordChangeForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "user@test.com"
        cls.current_password = "abcd123456"
        cls.new_password = "efghi7890"
        cls.user = get_user_model().objects.create_user(
            email=cls.email, password=cls.current_password
        )

    def test_matching_new_passwords(self):
        data = {
            "old_password": self.current_password,
            "new_password1": self.new_password,
            "new_password2": self.new_password
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_short_matching_new_passwords(self):
        data = {
            "old_password": self.current_password,
            "new_password1": "ab12",
            "new_password2": "ab12"
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_different_new_passwords(self):
        data = {
            "old_password": self.current_password,
            "new_password1": "1111111111",
            "new_password2": self.new_password
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_current_password_blank(self):
        data = {
            "old_password": "",
            "new_password1": self.new_password,
            "new_password2": self.new_password
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_new_password1_blank(self):
        data = {
            "old_password": self.current_password,
            "new_password1": "",
            "new_password2": self.new_password
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_new_password2_blank(self):
        data = {
            "old_password": self.current_password,
            "new_password1": self.new_password,
            "new_password2": ""
        }
        form = UserPasswordChangeForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_blank_passwords(self):
        data = {
            "old_password": "",
            "new_password1": "",
            "new_password2": ""
        }
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())


class TestUserPasswordResetConfirmForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="user@test.com", password="abcd123456"
        )

    def test_matching_new_passwords(self):
        new_password = "abcdefg12"
        data = {"new_password1": new_password, "new_password2": new_password}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_short_matching_new_passwords(self):
        new_password = "ab12"
        data = {"new_password1": new_password, "new_password2": new_password}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_different_new_passwords(self):
        data = {"new_password1": "Abcdefg12", "new_password2": "ab1234cdef"}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_new_password1_blank(self):
        data = {"new_password1": "", "new_password2": "ab1234cdef"}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_new_password2_blank(self):
        data = {"new_password1": "ab1234cdef", "new_password2": ""}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())

    def test_blank_passwords(self):
        data = {"new_password1": "", "new_password2": ""}
        form = UserPasswordResetConfirmForm(self.user, data=data)
        self.assertFalse(form.is_valid())
