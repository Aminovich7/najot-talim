from django.urls import path
from .views import index, list_category, create_category, delete_category, list_services, service_detail, category_detail, create_service, update_category, update_service, delete_service


urlpatterns = [
    path('', index, name='home'),
    path('list-category/', list_category, name = 'category-list'),
    path('detail-category/<int:id>', category_detail, name = 'category-detail'),
    path('create-category/', create_category, name = 'category-create'),
    path('update-category/<int:id>', update_category, name = 'category-update'),
    path('delete-category/<int:id>', delete_category, name = 'category-delete'),

    path('list-services/', list_services, name = 'service-list'),
    path('detail-service/<int:id>', service_detail, name = 'service-detail'),
    path('create-services/', create_service, name = 'service-create'),
    path('delete-services/<int:id>', delete_service, name = 'service-delete'),
    path('update-services/<int:id>', update_service, name = 'service-update')

]