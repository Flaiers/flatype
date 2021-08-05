from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.try_login),
    path('logout/', views.try_logout),
]
