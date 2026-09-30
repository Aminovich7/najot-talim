from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup", SignupView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("profile", ProfileView.as_view()),
    path("update-profile", UpdateProfile.as_view()),
    path("change_password", ChangePasswordView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
