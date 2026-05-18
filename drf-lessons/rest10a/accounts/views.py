from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt import exceptions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data": serializer.data, 
            "message": "User created successfully"
        })


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request=request, 
            username=serializer.validated_data.get("username"), 
            password=serializer.validated_data.get("password")
        )

        if not user:
            raise ValidationError({"detail": "Incorrect username or password!"})
        
        refresh_token = RefreshToken.for_user(user=user)

        return Response({
            "message": "Login successful",
            "access_token": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh = request.data.get("refresh")
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
        except exceptions.TokenError:
            return Response(
                {
                    "message": "Invalid refresh token",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )

        return Response(
            {
                "message": "Logged out successfully",
                "status": status.HTTP_204_NO_CONTENT
            }
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "email": user.email
        })


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileSerializer(
            instance=request.user, 
            data=request.data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        
        return Response({
            "data": serializer.data, 
            "message": "Profile updated successfully!"
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(
            context={"request": request}, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        
        return Response({
            "data": serializer.data, 
            "message": "Password changed successfully!"
        }, status=status.HTTP_200_OK)