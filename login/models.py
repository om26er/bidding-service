from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.settings import AUTH_USER_MODEL


class CustomUser(AbstractUser):
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    write_only = ('password',)
    USERNAME_FIELD = 'username'


class DummyModel(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='dummy')
    school = models.CharField(max_length=200)
