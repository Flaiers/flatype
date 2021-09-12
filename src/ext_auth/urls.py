from django.urls import path
from . import views


urlpatterns = [
    path('register', views.try_register, name='register'),
    path('logout', views.try_logout, name='logout'),
    path('login', views.try_login, name='login'),
    path('check', views.try_check, name='check'),
]
