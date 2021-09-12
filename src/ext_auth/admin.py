from .models import ExternalHashId

from django.contrib import admin
from django.contrib.sessions.models import Session

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


UserModel = get_user_model()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'get_decoded', 'expire_date',)


class ExternalHashIdInline(admin.TabularInline):
    model = ExternalHashId
    extra = 0


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fieldsets[0][1]['fields'] = ('username', 'link', 'password')

    inlines = [
        ExternalHashIdInline,
    ]


admin.register(ExternalHashId)
