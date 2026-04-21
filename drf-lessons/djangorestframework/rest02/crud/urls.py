from django.urls import path
from .views import WatchListView, WatchCreateView, WatchDetailView, WatchUpdateView, WatchDeleteView
#from .views import WatchListCreateView, WatchDetailUpdateDeleteView


urlpatterns = [

    path('list/', WatchListView.as_view()),
    path('create/', WatchCreateView.as_view()),
    path('detail/<int:pk>', WatchDetailView.as_view()),
    path('update/<int:pk>', WatchUpdateView.as_view()),
    path('delete/<int:pk>', WatchDeleteView.as_view()),

    # Boshqacha usul Urls:

    # path('list-create/', WatchListCreateView.as_view()),
    # path('detail-update-delete/<int:pk>', WatchDetailUpdateDeleteView.as_view()),

]