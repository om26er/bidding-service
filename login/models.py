from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    write_only = ('password',)
    USERNAME_FIELD = 'username'
