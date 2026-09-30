from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import SignUpSerializer, UserUpdateSerializer


class SignUpView(GenericAPIView):

    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Creates a new user account and returns the user data.",
        responses={
            201: SignUpSerializer,
            400: "Validation error",
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Account created successfully.", "user": serializer.data},
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Authenticate with username and password to receive a token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={"application/json": {"username": "john", "token": "abc123"}}
            ),
            400: "Invalid credentials",
        }
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ValidationError({"message": "Username and password are required."})

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({"message": "Invalid username or password."})

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"username": user.username, "token": token.key},
            status=status.HTTP_200_OK
        )


class UserProfileView(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get current user profile",
        operation_description="Returns the profile of the currently authenticated user.",
        responses={200: SignUpSerializer, 401: "Unauthorized"}
    )
    def get(self, request):
        serializer = SignUpSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


class UserUpdateView(GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Partially or fully update the authenticated user's profile.",
        responses={200: UserUpdateSerializer, 400: "Validation error", 401: "Unauthorized"}
    )
    def patch(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile updated successfully.", "user": serializer.data},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Replace user profile",
        operation_description="Fully replace the authenticated user's profile fields.",
        responses={200: UserUpdateSerializer, 400: "Validation error", 401: "Unauthorized"}
    )
    def put(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile replaced successfully.", "user": serializer.data},
            status=status.HTTP_200_OK
        )


class UserDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete user account",
        operation_description="Permanently deletes the currently authenticated user and invalidates their token.",
        responses={204: "Account deleted", 401: "Unauthorized"}
    )
    def delete(self, request):
        user = request.user
        # Revoke token before deletion
        Token.objects.filter(user=user).delete()
        user.delete()
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )