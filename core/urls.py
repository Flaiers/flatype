from django.urls import path
from . import views


urlpatterns = [
    path('', views.create_new, name = 'create_new'),
    path('vremya-raboty-iyul-07-19', views.test, name = 'viewing')
]

handler404 = views.Exceptions().page_not_found
handler500 = views.Exceptions().server_error
handler400 = views.Exceptions().bad_request
handler403 = views.Exceptions().permission_denied
