from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_new, name = 'create_new'),
    path('404', views.page_404, name = 'page_404')
]
