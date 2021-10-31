from apps.api import views as views_api

from django.urls import path


urlpatterns = [
    path('upload', views_api.try_upload, name='upload'),
    path('save', views_api.try_save, name='save'),
]
