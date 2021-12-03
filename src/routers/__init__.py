from .main_router import urlpatterns as main
from .core_router import urlpatterns as core

from django.conf import settings
from django.contrib import admin


urlpatterns = main + core

admin.site.site_header = "Flatype Admin"
admin.site.site_title = "Flatype Admin"
admin.site.index_title = "Welcome to flatype Admin Panel"

handler400 = "apps.core.exceptions.bad_request"
handler403 = "apps.core.exceptions.permission_denied"
handler404 = "apps.core.exceptions.page_not_found"
handler500 = "apps.core.exceptions.server_error"

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
