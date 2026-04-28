from django.urls import path
from .views import CustomLoginView, RegisterView, ProfileUpdateView, logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('logout/', logout_view, name='logout'),
]