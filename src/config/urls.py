import debug_toolbar

from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', include('ext_auth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', include('core.urls')),
]

admin.site.site_header = "Flatype Admin Panel"
admin.site.site_title = "Flatype Admin"
admin.site.index_title = "Welcome to Flatype Admin Panel"

if settings.DEBUG:
    from django.conf.urls.static import static


    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
