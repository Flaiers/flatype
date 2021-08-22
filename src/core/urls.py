from django.urls import path

from . import views


urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('<slug:slug>', views.View.as_view(), name='view'),
]
