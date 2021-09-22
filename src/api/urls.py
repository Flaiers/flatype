from django.urls import path

from . import views


urlpatterns = [
    path('__upload', views.try_upload, name='upload'),
    path('__save', views.try_save, name='save'),
]
