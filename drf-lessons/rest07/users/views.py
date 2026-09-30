from rest_framework import status, views, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .serializers import AuthorSerializer

class AuthorSignupView(generics.CreateAPIView):
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)

class AuthorLoginView(views.APIView):
    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user:
            login(request, user)
            return Response({"detail": "Logged in successfully."})
        return Response({"detail": "Invalid credentials."}, status=401)