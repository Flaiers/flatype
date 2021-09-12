from .models import ExternalHashId

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model, admin as auth_admin


UserModel = get_user_model()


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def get_session_data(self, obj): return obj.get_decoded()
    get_session_data.short_description = 'session data'

    list_display = ('session_key', 'get_session_data', 'expire_date',)


class ExternalHashIdInline(admin.TabularInline):
    model = ExternalHashId
    extra = 0


class UserAdmin(auth_admin.UserAdmin):
    auth_admin.UserAdmin.fieldsets[0][1]['fields'] = ('username', 'user_link', 'password')

    inlines = [
        ExternalHashIdInline,
    ]


admin.site.register(UserModel, UserAdmin)
admin.register(ExternalHashId)
