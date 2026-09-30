from django.urls import path

from .views import ToolListView, ToolCreateView, ToolDetailView, ToolDeleteView, ToolUpdateView

urlpatterns = [

    path('list/', ToolListView.as_view()),
    path('create/', ToolCreateView.as_view()),
    path('detail/<int:pk>', ToolDetailView.as_view()),
    path('delete/<int:pk>', ToolDeleteView.as_view()),
    path('update/<int:pk>', ToolUpdateView.as_view()),

]