from django.urls import path
from .views import list_category, create_category, delete_category, list_services, create_service, delete_service


urlpatterns = [
    path('', 'home.html'),
    path('list-category', list_category, name = 'category-list'),
    path('create-category/', create_category, name = 'category-create'),
    path('delete-category/', delete_category, name = 'category-delete'),
    path('list-services', list_services, name = 'service-list'),
    path('create-services', create_service, name = 'service-create'),
    path('delete-services', delete_service, name = 'service-delete'),

]