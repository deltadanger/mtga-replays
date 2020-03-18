from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from api.views import GamesViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r'games', GamesViewSet, basename='game')

urlpatterns = [
    url(r'^', include(router.urls)),
]
