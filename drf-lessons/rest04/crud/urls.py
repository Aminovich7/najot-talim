from django.urls import path
from crud.views import WatchGenericApiView

urlpatterns = [
    path('generic/', WatchGenericApiView.as_view(), name='generic'),
    path('generic/<int:pk>', WatchGenericApiView.as_view(), name='generic'),
]