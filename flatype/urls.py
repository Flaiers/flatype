"""flatype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('core/', include('core.urls'))
"""
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
