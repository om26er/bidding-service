from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.settings import MEDIA_ROOT


class CustomUser(AbstractUser):
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=MEDIA_ROOT)

    write_only = ('password',)
    USERNAME_FIELD = 'username'


# class ProductAd(models.Model):