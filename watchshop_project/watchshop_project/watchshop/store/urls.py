from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('my-watches/', views.my_products_view, name='my_products'),
    path('my-watches/add/', views.product_create_view, name='product_create'),
    path('my-watches/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('my-watches/<int:pk>/delete/', views.product_delete_view, name='product_delete'),
]
