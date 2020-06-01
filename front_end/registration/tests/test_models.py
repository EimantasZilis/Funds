from django.contrib.auth import get_user_model
from django.test import TestCase


class MyUserManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_email = "user@test.com"
        cls.superuser_email = "admin@test.com"
        cls.password = "abcd123456"

        user_model = get_user_model()
        cls.create_user = user_model.objects.create_user
        cls.create_superuser = user_model.objects.create_superuser

    def test_create_user(self):
        user = self.create_user(email=self.user_email, password=self.password)
        self.assertEqual(user.email, self.user_email)
        self.assertIsNotNone(user.password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        with self.assertRaises(AttributeError):
            user.username

    def test_create_user_blank_email(self):
        with self.assertRaises(ValueError):
            self.create_user(email="", password=self.password)

    def test_create_user_default_password(self):
        with self.assertRaises(ValueError):
            self.create_user(email=self.user_email)

    def test_create_user_blank_password(self):
        with self.assertRaises(ValueError):
            self.create_user(email=self.user_email, password="")

    def test_create_superuser(self):
        superuser = self.create_superuser(
            email=self.superuser_email, password=self.password
        )
        self.assertEqual(superuser.email, self.superuser_email)
        self.assertIsNotNone(superuser.password)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        with self.assertRaises(AttributeError):
            superuser.username

    def test_create_superuser_default_password(self):
        with self.assertRaises(ValueError):
            self.create_superuser(email=self.superuser_email)

    def test_create_superuser_blank_email(self):
        with self.assertRaises(ValueError):
            self.create_superuser(email="", password=self.password)

    def test_create_superuser_blank_password(self):
        with self.assertRaises(ValueError):
            self.create_superuser(email=self.superuser_email, password="")
