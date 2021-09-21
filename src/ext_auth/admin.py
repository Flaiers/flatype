from django.contrib import admin
from django.contrib.sessions.models import Session

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ProxyUser


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'get_decoded', 'expire_date',)


@admin.register(ProxyUser)
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'link', 'password')
