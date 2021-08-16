from django.urls import path

from .views import Exceptions
from . import views


urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('<slug:slug>', views.View.as_view(), name='view'),
]

e = Exceptions()

handler400 = e.bad_request
handler403 = e.permission_denied
handler404 = e.page_not_found
handler500 = e.server_error
