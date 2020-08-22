from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'nick_name', 'email', 'is_staff', 'is_active', 'is_superuser')

    def nick_name(self, obj):
        return obj.profile.nick_name
    nick_name.short_description = '昵称'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'nick_name'
    ]
