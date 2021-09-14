from django.contrib import admin
from django.contrib.sessions.models import Session

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


UserModel = get_user_model()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'get_decoded', 'expire_date',)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'link', 'password')
