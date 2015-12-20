from django.contrib import admin

from login.models import customuser


class UserProfileAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name_plural = 'userprofile'

admin.site.register(customuser, UserProfileAdmin)
