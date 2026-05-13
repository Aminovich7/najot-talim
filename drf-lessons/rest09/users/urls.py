from .views import (
    SignUpView,
    LoginView,
    UserProfileView,
    UserProfileUpdateleView,
    UserChangePasswordView,
    LogoutView,
    ProfileDeleteView,
)
from django.urls import path

urlpatterns = [
    path("sign-up/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/<int:pk>", UserProfileView.as_view()),
    path("profile-delete/<int:pk>", ProfileDeleteView.as_view()),
    path("update-profile/<int:pk>", UserProfileUpdateleView.as_view()),
    path("change-password/<int:pk>", UserChangePasswordView.as_view()),
]
