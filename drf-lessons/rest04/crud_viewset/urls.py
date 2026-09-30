from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchViewSet # WatchModelViewSet

router = DefaultRouter()

router.register(r'viewset', WatchViewSet, basename='viewset')


#MODEL VIEWSET UCHUN COMMENTDAN OCHING
# router.register(r'viewset', WatchModelViewSet, basename='viewset')

urlpatterns = [
    path('', include(router.urls)),
]