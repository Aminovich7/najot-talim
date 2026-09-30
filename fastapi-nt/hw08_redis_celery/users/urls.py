from django.urls import path
from .views import (
    SignupView, 
    LoginView, 
    LogoutView,
    ProfileApiView, 
    UpdateProfileApiView, 
    ChangePasswordapiView, 
    UserDeleteApiView,
    DepositMoneyView,
    BuyPremiumView
)

urlpatterns = [
    # Auth 
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

 
    path('profile/', ProfileApiView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileApiView.as_view(), name='profile-update'),
    path('profile/change-password/', ChangePasswordapiView.as_view(), name='change-password'),
    path('profile/delete/', UserDeleteApiView.as_view(), name='account-delete'),

    # Wallet
    path('wallet/deposit/', DepositMoneyView.as_view(), name='deposit-money'),
    path('premium/buy/', BuyPremiumView.as_view(), name='buy-premium'),
]