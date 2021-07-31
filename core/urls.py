from django.urls import path

from .views import Exceptions
from . import views


urlpatterns = [
    path('', views.create_new, name='create_new'),
    path('<slug:slug>/', views.viewing, name='viewing'),
]

classExcept = Exceptions()

handler404 = classExcept.page_not_found
handler500 = classExcept.server_error
handler400 = classExcept.bad_request
handler403 = classExcept.permission_denied
