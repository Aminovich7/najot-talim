from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer


class PostListCreateView(APIView):
    # GET: Hamma postlarni ko'rish (Ruxsat shart emas)
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # POST: Yangi post yaratish (Faqat login qilganlar uchun)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Avval tizimga kiring!"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailUpdateDeleteView(APIView):
    # GET: Bitta postni ko'rish
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # PUT: Postni tahrirlash (Faqat muallif uchun)
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Permission o'rniga qo'lda tekshirish:
        if not request.user.is_authenticated:
            return Response({"detail": "Tizimga kirmagansiz!"}, status=401)
        if post.author != request.user:
            return Response({"detail": "Siz faqat o'z postingizni tahrirlay olasiz!"}, status=403)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE: Postni o'chirish (Faqat muallif uchun)
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Permission o'rniga qo'lda tekshirish:
        if not request.user.is_authenticated:
            return Response({"detail": "Tizimga kirmagansiz!"}, status=401)
        if post.author != request.user:
            return Response({"detail": "Sizda buni o'chirishga ruxsat yo'q!"}, status=403)

        post.delete()
        return Response({"detail": "Post o'chirildi"}, status=status.HTTP_204_NO_CONTENT)