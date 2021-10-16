from django.urls import path

from . import views


urlpatterns = [
    path('upload', views.try_upload, name='upload'),
    path('save', views.try_save, name='save'),
]
