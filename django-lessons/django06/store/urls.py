from django.urls import path
from .views import (
    PhoneListView,
    PhoneCreateView,
    PhoneUpdateView,
    PhoneDeleteView
)

urlpatterns = [
    path('', PhoneListView.as_view(), name='phone-list'),
    path('add/', PhoneCreateView.as_view(), name='phone-add'),
    path('edit/<int:pk>/', PhoneUpdateView.as_view(), name='phone-edit'),
    path('delete/<int:pk>/', PhoneDeleteView.as_view(), name='phone-delete'),
]