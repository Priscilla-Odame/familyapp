from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from phone_field import PhoneField

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, firstname, surname, maidenname, phone, email, password=None):
        if firstname is None:
            raise TypeError("Users should have firstname")
        if surname is None:
            raise TypeError("Users should have surname")
        if email is None:
            raise TypeError("User should have an email")

        user = self.model(
            firstname=firstname,
            surname=surname,
            maidenname=maidenname,
            phone=phone,
            email=email
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, firstname, surname, maidenname, phone, email, password):
        if firstname is None:
            raise TypeError("Users should have firstname")
        if surname is None:
            raise TypeError("Users should have surname")
        if password is None:
            raise TypeError("Users should have password")

        user = self.create_user(
            firstname=firstname,
            surname=surname,
            maidenname=maidenname,
            phone=phone,
            email=email
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField('First name', max_length=100)
    surname = models.CharField('Surname', max_length=100)
    maidenname = models.CharField('Maiden Name', max_length=100)
    phone = PhoneField('Phone number', blank=True)
    email = models.EmailField('Email', max_length=100, unique=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    last_login = models.DateTimeField('last joined', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'surname', 'phone', 'maidenname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
