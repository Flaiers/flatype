from django.urls import path
from . import views

urlpatterns = [
    path('__login/', views.try_login),
    path('__logout/', views.try_logout),
]
