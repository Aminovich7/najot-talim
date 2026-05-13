from .serializers import (
    CreateBlogSerializer,
    BlogDetailSerializer,
    UpdateBlogSerializer,
    CreateCommentSerializer,
    UpdateCommentSerializer,
)
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from users.permissions import IsAuthorOrReadOnly, IsUserOrAdminForComment


class CreateBlogView(GenericAPIView):
    serializer_class = CreateBlogSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

        return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})


class BlogDetailView(GenericAPIView):
    serializer_class = BlogDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        serializer = self.get_serializer(blog)

        return Response(
            {
                "message": "Detail",
                "data": serializer.data,
            }
        )


class UpdateBlogView(GenericAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = UpdateBlogSerializer

    def patch(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        self.check_object_permissions(request, blog)
        serializer = self.get_serializer(blog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Blog update successfully!"})


class DeleteBlogView(GenericAPIView):
    permission_classes = [IsAuthorOrReadOnly]

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        self.check_object_permissions(request, blog)
        blog.delete()

        return Response(
            {
                "message": "Blog Deleted!",
                "status": status.HTTP_204_NO_CONTENT,
            }
        )


class CreateCommentView(GenericAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

        return Response(
            {serializer.data},
            status.HTTP_201_CREATED,
        )


class UpdateCommentView(GenericAPIView):
    serializer_class = UpdateCommentSerializer
    permission_classes = [IsUserOrAdminForComment]

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Comment updated")


class DeleteCommentView(GenericAPIView):
    permission_classes = [IsUserOrAdminForComment]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()

        return Response("Comment deleted")
