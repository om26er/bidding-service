from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.settings import AUTH_USER_MODEL

AD_IMAGES = 'attachments'


class CustomUser(AbstractUser):
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='avatars')
    interests = models.CharField(max_length=1000, blank=True)
    push_key = models.CharField(max_length=1000, blank=True)

    write_only = ('password',)
    USERNAME_FIELD = 'username'


class ProductAd(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='ad')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=70, blank=False)
    description = models.CharField(max_length=4000, blank=False)
    category = models.CharField(max_length=100, blank=False)
    price = models.CharField(max_length=10, blank=False)
    photo1 = models.ImageField(upload_to=AD_IMAGES)
    photo2 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo3 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo4 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo5 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo6 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo7 = models.ImageField(upload_to=AD_IMAGES, blank=True)
    photo8 = models.ImageField(upload_to=AD_IMAGES, blank=True)
