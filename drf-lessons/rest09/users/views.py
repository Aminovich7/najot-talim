from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer,
)
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView
from .models import CustomUser


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"response": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]

        return Response(
            {
                "usernam": user.username,
                "token": token.key,
                "status": status.HTTP_200_OK,
            }
        )


class UserProfileView(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                "user": serializer.data,
                "status": status.HTTP_200_OK,
            }
        )


class UserProfileUpdateleView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserChangePasswordView(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):

        serializer = UserChangePasswordSerializer(
            context={"request": request}, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Message": "Parollar ozgartirildi"}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response({"message": "Logout", "status": status.HTTP_204_NO_CONTENT})


class ProfileDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        user = request.user

        if hasattr(user, "auth_token"):
            user.auth_token.delete()

        user.delete()

        return Response(
            {"message": "Profile deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
