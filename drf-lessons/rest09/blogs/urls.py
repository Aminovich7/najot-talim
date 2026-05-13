from django.urls import path

from .views import (
    CreateBlogView,
    BlogDetailView,
    UpdateBlogView,
    DeleteBlogView,
    CreateCommentView,
    UpdateCommentView,
    DeleteCommentView,
)

urlpatterns = [
    path("blog-create/", CreateBlogView.as_view()),
    path("blog-detail/<int:pk>", BlogDetailView.as_view()),
    path("blog-update/<int:pk>", UpdateBlogView.as_view()),
    path("blog-delete/<int:pk>", DeleteBlogView.as_view()),
    ### Comments
    path("comment-create/", CreateCommentView.as_view()),
    path("comment-update/<int:pk>", UpdateCommentView.as_view()),
    path("comment-delete/<int:pk>", DeleteCommentView.as_view()),
]
