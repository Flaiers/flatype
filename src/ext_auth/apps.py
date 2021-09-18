from django.apps import AppConfig

from django.contrib.auth.apps import AuthConfig as BaseAuthConfig


class AuthConfig(BaseAuthConfig):
    verbose_name = 'Groups'


class ExtAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ext_auth'
    verbose_name = "Users"

