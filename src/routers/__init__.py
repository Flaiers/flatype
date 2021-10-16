from django.conf import settings

from django.contrib import admin

from .main_router import urlpatterns as main


urlpatterns = main

admin.site.site_header = "Flatype Admin"
admin.site.site_title = "Flatype Admin"
admin.site.index_title = "Welcome to Flatype Admin Panel"

handler400 = "core.exceptions.bad_request"
handler403 = "core.exceptions.permission_denied"
handler404 = "core.exceptions.page_not_found"
handler500 = "core.exceptions.server_error"

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
