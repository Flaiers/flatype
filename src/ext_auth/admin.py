from .models import ExternalHashId

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model, admin as auth_admin


actual_user_model = get_user_model()


class SessionAdmin(admin.ModelAdmin):
    get_session_data = lambda self, obj: obj.get_decoded()
    get_session_data.short_description = 'session data'

    list_display = ['session_key', 'get_session_data', 'expire_date']


class ExternalHashIdInline(admin.TabularInline):
    model = ExternalHashId
    extra = 0


class UserAdmin(auth_admin.UserAdmin):

    inlines = [
        ExternalHashIdInline,
    ]


admin.site.unregister(actual_user_model)
admin.site.register(actual_user_model, UserAdmin)
admin.site.register(Session, SessionAdmin)

admin.register(ExternalHashId)
