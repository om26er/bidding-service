import uuid
import os

from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models

from accounts.settings import AUTH_USER_MODEL

CHOICES = [(i, i) for i in range(1, 6)]


def get_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4(), ext)
    return os.path.join('images', filename)


class CustomUser(AbstractUser):
    created = models.DateTimeField(auto_now_add=True, null=True)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=get_image_file_path)
    interests = models.CharField(max_length=1000, blank=True)
    push_key = models.CharField(max_length=1000, blank=True)

    write_only = ('password',)
    USERNAME_FIELD = 'username'


class ProductAd(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, blank=False, related_name='ad')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=70, blank=False)
    description = models.CharField(max_length=4000, blank=False)
    category = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    photo1 = models.ImageField(upload_to=get_image_file_path)
    photo2 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo3 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo4 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo5 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo6 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo7 = models.ImageField(upload_to=get_image_file_path, blank=True)
    photo8 = models.ImageField(upload_to=get_image_file_path, blank=True)

    class Meta:
        ordering = ('created', )

    def __unicode__(self):
        return '{} at {}'.format(self.title, self.price)


class ProductAdInline(admin.TabularInline):

    model = ProductAd


class Comments(models.Model):

    ad = models.ForeignKey(ProductAd, related_name='comments')
    review = models.CharField(max_length=2000, blank=True)
    stars = models.IntegerField(choices=CHOICES, blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return '{}: {}'.format(self.review, self.stars)


class AdCommentsInline(admin.TabularInline):
    model = Comments


class AdCategories(models.Model):

    name = models.CharField(max_length=70, blank=False, unique=True)
    photo = models.ImageField(upload_to=get_image_file_path, blank=False)
    id = models.AutoField(primary_key=True)
