from django.shortcuts import render
from .models import Post, Comment
from users.models import CustomUser
from rest_framework import status, permissions
from rest_framework.views import APIView
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, CommentCreateSerializer, CommentSerializer, CategorySerializer
from rest_framework.response import Response
from .permissions import IsAdmin, IsOwner, IsPremiumUser
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


class CreateCategoryApiView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostListApiView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=PostSerializer, responses=PostSerializer)
    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many = True, context = {"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=PostCreateSerializer, responses=PostCreateSerializer)
    def post(self, request):
        serializer = PostCreateSerializer(data = request.data, context = {"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPremiumUser]

    @extend_schema(request=PostSerializer, responses=PostSerializer)
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        self.check_object_permissions(request, post)
        
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)



class PostUpdateApiView(APIView):

    permission_classes = [IsOwner]

    @extend_schema(request=PostUpdateSerializer, responses=PostUpdateSerializer)
    def put(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        serializer = PostUpdateSerializer(data = request.data, instance = post, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class PostDeleteApiView(APIView):
    permission_classes = [IsOwner]
    
    @extend_schema(
        request=None, 
        responses={204: None, 404: None}, # 204 No Content qaytishi kutiladi
        description="Postni o'chirish uchun ishlatiladi. Body talab qilinmaydi."
    )
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({"message":"Post o'chirildi"})
    

class CommentCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=CommentCreateSerializer, responses=CommentCreateSerializer)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.is_premium and not request.user.is_premium_active:
            return Response(
                {"error": "Premium postga faqat premium a'zolar izoh yoza oladi."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
