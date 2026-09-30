from django.urls import path
from .views import WatchCreateView, WatchUpdateView, WatchSearchView

urlpatterns = [
    path('create/', WatchCreateView.as_view()),
    path('search/', WatchSearchView.as_view()),
    path('update/<int:pk>', WatchUpdateView.as_view())

]