from django.contrib import admin

from login.models import CustomUser, ProductAd, AdCategories


class UserProfileAdmin(admin.ModelAdmin):
    can_delete = False
    verbose_name_plural = 'userprofile'
    list_per_page = 15
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'created', 'is_active')


class AdAdmin(admin.ModelAdmin):
    can_delete = True
    verbose_name_plural = 'product ad'
    list_per_page = 15
    list_display = ('title', 'created')


admin.site.register(CustomUser, UserProfileAdmin)
admin.site.register(ProductAd, AdAdmin)
admin.site.register(AdCategories)
