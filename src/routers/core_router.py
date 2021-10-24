from django.urls import path

from apps.core import views as views_core


urlpatterns = [
    path('', views_core.Create.as_view(), name='create'),
    path('<slug:slug>', views_core.View.as_view(), name='view'),
]
