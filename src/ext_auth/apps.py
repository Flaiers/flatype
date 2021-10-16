from django.apps import AppConfig
from packs import rename_tables


class ExtAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ext_auth'
    verbose_name = 'Authentication and Authorization'

    def ready(self):
        # Rename standard models db_table to my
        rename_tables()
