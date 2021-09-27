from django.contrib import admin
from django.contrib.sessions.models import Session

from django.contrib.auth.admin import (
        UserAdmin as BaseUserAdmin,
        GroupAdmin as BaseGroupAdmin,
    )
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import ProxyGroup, ProxyLogEntry


UserModel = get_user_model()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fields = ('session_key', 'session_data', 'expire_date',)
    list_display = ('session_key', 'get_decoded', 'expire_date',)
    search_fields = ('session_key',)
    date_hierarchy = 'expire_date'
    ordering = ('-expire_date',)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'link', 'password')


@admin.register(ProxyGroup)
class GroupAdmin(BaseGroupAdmin):
    fields = ('name', 'permissions',)
    list_display = ('name',)


@admin.register(ProxyLogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def get_message(self, obj): return obj
    get_message.short_description = 'message'

    list_display = ('get_message', 'action_time',)
    list_filter = ('action_flag', 'content_type',)
    search_fields = ('user', 'change_message',)
    date_hierarchy = 'action_time'
    ordering = ('-action_time',)


admin.site.unregister(Group)
