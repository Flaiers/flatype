from django.urls import path

from .views import Exceptions
from . import views


urlpatterns = [
    path('', views.create_new, name='create_new'),
    path('<slug:slug>', views.viewing, name='viewing'),
]

e = Exceptions()

handler400 = e.bad_request
handler403 = e.permission_denied
handler404 = e.page_not_found
handler500 = e.server_error
