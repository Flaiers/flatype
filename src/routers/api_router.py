from django.urls import path

from apps.api import views as views_api


urlpatterns = [
    path('upload', views_api.try_upload, name='upload'),
    path('save', views_api.try_save, name='save'),
]
