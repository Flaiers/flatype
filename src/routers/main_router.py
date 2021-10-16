from django.urls import include, path

from django.contrib import admin


urlpatterns = [
    path('auth/', include('routers.auth_router')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('routers.api_router')),
]
