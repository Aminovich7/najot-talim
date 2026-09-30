from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsOwnerprofile
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from decimal import Decimal
from .constants import PREMIUM_SUBSCRIPTION_PRICE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, ChangePasswordSerializer, AccountDeleteSerializer, DepositSerializer
from drf_spectacular.utils import extend_schema



class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=SignupSerializer, responses=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "Tabriklaymiz! Ro'yxatdan muvaffaqiyatli o'tdingiz.",
                "token": token.key,
                "user_id": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=LoginSerializer, responses=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "token": token.key,
                "username": user.username,
                "is_premium": user.is_premium
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerprofile]

    @extend_schema(request=ProfileUpdateSerializer, responses=ProfileUpdateSerializer)
    def put(self, request): 
        user = request.user 
        self.check_object_permissions(request, user)
        serializer = ProfileUpdateSerializer(instance=user, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordapiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, responses=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():   
            serializer.save()
            return Response(
                {"message": "Parol muvaffaqiyatli o'zgartirildi."}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=AccountDeleteSerializer, responses=AccountDeleteSerializer)
    def post(self, request):
        serializer = AccountDeleteSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.delete()
            return Response(
                {"message": "Akkaunt muvaffaqiyatli o'chirildi."},
                status=status.HTTP_200_OK 
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        request=None, 
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
        description="Foydalanuvchining joriy tokenini o'chiradi va tizimdan chiqaradi."
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Tizimdan muvaffaqiyatli chiqildi."}, 
            status=status.HTTP_200_OK)
 

class DepositMoneyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=DepositSerializer,
        responses={200: {"properties": {"message": {"type": "string"}, "new_balance": {"type": "number"}}}}
    )
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data['amount']
        
        wallet = request.user.wallet
        wallet.balance += amount
        wallet.save()

        return Response({
            "message": f"Hamyon {amount} so'mga to'ldirildi.",
            "new_balance": wallet.balance
        })


class BuyPremiumView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    price = PREMIUM_SUBSCRIPTION_PRICE

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Premium obuna muvaffaqiyatli rasmiylashtirildi!"},
                    "expires_at": {"type": "string", "format": "date-time"},
                    "remaining_balance": {"type": "number", "example": 5500.50}
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Mablag' yetarli emas!"}
                }
            }
        },
        summary="Premium obuna sotib olish",
        description="Foydalanuvchi hamyonidan belgilangan summani yechib, premium muddatini 30 kunga uzaytiradi."
    )
    def post(self, request):
        user = request.user
        wallet = user.wallet

        if wallet.balance < self.price:
            return Response({"error": "Mablag' yetarli emas!"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            wallet.balance -= Decimal(f"{self.price}")
            wallet.save()

            now = timezone.now()

            # Agar obuna hali tugamagan bo'lsa, ustiga 30 kun qo'shamiz
            if user.premium_expires_at and user.premium_expires_at > now:
                user.premium_expires_at += timedelta(days=30)
            else:
                user.premium_expires_at = now + timedelta(days=30)
            
            user.is_premium = True
            user.save()

        return Response({
            "message": "Premium obuna muvaffaqiyatli rasmiylashtirildi!",
            "expires_at": user.premium_expires_at,
            "remaining_balance": wallet.balance
        })

