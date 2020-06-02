from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


"""
This was copied from https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
According to documentation, this model would be compatible with all the built-in auth forms and views,
except for the user creation forms. It is not intended to be copied directly into projects for
production use. 

Why?
"""


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users cannot have a blank password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Superusers must have an email address")

        if not password:
            raise ValueError("Superusers cannot have a blank password")

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", unique=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label=None):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
