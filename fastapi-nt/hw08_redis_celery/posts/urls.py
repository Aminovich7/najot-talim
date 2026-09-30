from django.urls import path
from .views import *
urlpatterns = [
    path("crete-category/", CreateCategoryApiView.as_view()),
    path("", PostListApiView.as_view()),
    path("post-create/", PostCreateApiView.as_view()),
    path("comment-create/<int:post_id>/comment/", CommentCreateApiView.as_view()),
    path("post-detail/<int:pk>/", PostDetailApiView.as_view()),
    path("post-update/<int:pk>/", PostUpdateApiView.as_view()),
    path("post-delete/<int:pk>/", PostDeleteApiView.as_view()),


]
