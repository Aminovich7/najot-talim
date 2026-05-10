from django.urls import path
from .views import SignUpView, LoginView, UserProfileView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('signup/',         SignUpView.as_view(),      name='signup'),
    path('login/',          LoginView.as_view(),       name='login'),
    path('',             UserProfileView.as_view(), name='user-profile'),
    path('update/',      UserUpdateView.as_view(),  name='user-update'),
    path('delete/',      UserDeleteView.as_view(),  name='user-delete'),
]