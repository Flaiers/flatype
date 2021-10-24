from django.contrib import admin

from django.contrib.sessions.models import Session

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (
        UserAdmin as BaseUserAdmin,
        GroupAdmin as BaseGroupAdmin,
    )

from .models import ProxyGroup, ProxyLogEntry

import copy


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

    list_display = ('username', 'email', 'is_superuser', 'is_active')
    readonly_fields = ('link',)

    def get_fieldsets(self, request, obj):
        fieldsets = copy.deepcopy(self.fieldsets)
        fieldsets[0][1]['fields'] = ('username', 'link', 'password')
        return fieldsets


@admin.register(ProxyGroup)
class GroupAdmin(BaseGroupAdmin):

    fields = ('name', 'permissions',)
    list_display = ('name',)


@admin.register(ProxyLogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    list_display = ('get_message', 'user', 'action_time',)
    search_fields = ('user', 'object_repr', 'change_message',)
    list_filter = ('action_flag', 'content_type',)
    autocomplete_fields = ('user',)
    date_hierarchy = 'action_time'
    ordering = ('-action_time',)

    def get_message(self, obj): return obj
    get_message.short_description = 'message'


admin.site.unregister(Group)
