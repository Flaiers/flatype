from django.urls import path

from ext_auth import views as views_auth


urlpatterns = [
    path('register', views_auth.try_register, name='register'),
    path('logout', views_auth.try_logout, name='logout'),
    path('login', views_auth.try_login, name='login'),
    path('check', views_auth.try_check, name='check'),
]
