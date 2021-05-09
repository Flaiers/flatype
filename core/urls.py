from django.urls import path

from . import views

urlpatterns = [
    path('hi', views.index, name = 'hi'),
    path('', views.create, name = 'create')
]
