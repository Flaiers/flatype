from django.contrib import admin

from .models import ExternalHashId
from django.contrib.auth import get_user_model, admin as auth_admin


actual_user_model = get_user_model()


class ExternalHashIdInline(admin.TabularInline):
    model = ExternalHashId
    extra = 0


class UserAdmin(auth_admin.UserAdmin):

    inlines = [
        ExternalHashIdInline,
    ]


admin.site.unregister(actual_user_model)
admin.site.register(actual_user_model, UserAdmin)

admin.register(ExternalHashId)
