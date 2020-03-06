from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


router = DefaultRouter() if settings.DEBUG else SimpleRouter()


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^board$', views.BoardView.as_view()),
]
