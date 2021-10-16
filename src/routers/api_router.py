from rest_framework.routers import DefaultRouter

from api import views as views_api


router = DefaultRouter(trailing_slash=False)
router.register('auth', views_api.AuthViewSet)
router.register('user', views_api.UserDataViewSet)

urlpatterns = router.urls
