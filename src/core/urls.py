from django.urls import path

from . import views


urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('<slug:slug>', views.View.as_view(), name='view'),
]


handler400 = "core.exceptions.bad_request"
handler403 = "core.exceptions.permission_denied"
handler404 = "core.exceptions.page_not_found"
handler500 = "core.exceptions.server_error"
