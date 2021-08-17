from django.urls import path

from . import exceptions, views


urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('<slug:slug>', views.View.as_view(), name='view'),
]


handler400 = exceptions.bad_request
handler403 = exceptions.permission_denied
handler404 = exceptions.page_not_found
handler500 = exceptions.server_error
