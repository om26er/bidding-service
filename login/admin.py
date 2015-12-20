from django.contrib import admin

from login.models import CustomUser


class UserProfileAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name_plural = 'userprofile'

admin.site.register(CustomUser, UserProfileAdmin)
