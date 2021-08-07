from django.urls import path
from . import views


urlpatterns = [
    path('__register/', views.try_register, name='register'),
    path('__login/', views.try_login, name='login'),
    path('__logout/', views.try_logout, name='logout'),
    path('__save/', views.try_save, name='save'),
    path('__edit/', views.try_edit, name='edit'),
]
