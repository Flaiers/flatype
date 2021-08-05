from django.urls import path
from . import views


urlpatterns = [
    path('__save/', views.save, name='save'),
]
