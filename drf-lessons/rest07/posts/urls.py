from django.urls import path
from .views import PostListCreateView, PostDetailUpdateDeleteView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailUpdateDeleteView.as_view(), name='post-detail'),
]