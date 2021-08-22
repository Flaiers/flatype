from django.urls import path

from . import views


urlpatterns = [
    path('__register/', views.try_register, name='register'),
    path('__upload/', views.try_upload, name='upload'),
    path('__save/', views.try_save, name='save'),
]
