from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('auth/', include('ext_auth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', include('core.urls')),
]

admin.site.site_header = "Flatype Admin Panel"
admin.site.site_title = "Flatype Admin"
admin.site.index_title = "Welcome to Flatype Admin Panel"

if settings.DEBUG:
    from django.conf.urls import url
    from django.views import static

    urlpatterns.append(url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}))
    urlpatterns.append(url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}))
