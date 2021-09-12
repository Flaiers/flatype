from .models import ExternalHashId, Group

from django.contrib import admin
from django.contrib.sessions.models import Session

from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as BaseGroup


UserModel = get_user_model()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def get_session_data(self, obj): return obj.get_decoded()
    get_session_data.short_description = 'session data'

    list_display = ('session_key', 'get_session_data', 'expire_date',)


class ExternalHashIdInline(admin.TabularInline):
    model = ExternalHashId
    extra = 0


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'link', 'password')

    inlines = [
        ExternalHashIdInline,
    ]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


admin.site.unregister(BaseGroup)
admin.register(ExternalHashId)
