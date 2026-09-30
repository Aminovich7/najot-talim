from django.urls import path
from .views import *

urlpatterns = [
    path('', TotalReportView.as_view(), name='home'),
    # Doctor URLs

    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('doctors/<int:pk>/update/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor-delete'),

    # Consultation URLs
    path('consultations/', ConsultationListView.as_view(), name='consultation-list'),
    path('consultations/create/', ConsultationCreateView.as_view(), name='consultation-create'),
    path('consultations/<int:pk>/update/', ConsultationUpdateView.as_view(), name='consultation-update'),
    path('consultations/<int:pk>/delete/', ConsultationDeleteView.as_view(), name='consultation-delete'),

    # Surgery URLs
    path('surgeries/', SurgeryListView.as_view(), name='surgery-list'),
    path('surgeries/create/', SurgeryCreateView.as_view(), name='surgery-create'),
    path('surgeries/<int:pk>/update/', SurgeryUpdateView.as_view(), name='surgery-update'),
    path('surgeries/<int:pk>/delete/', SurgeryDeleteView.as_view(), name='surgery-delete'),

    # Room URLs
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),

    # Report URLs
    path('consultation-report/', ConsultationReportView.as_view(), name='consultation-report'),
    path('surgery-report/', SurgeryReportView.as_view(), name='surgery-report'),
    path('room-report/', RoomReportView.as_view(), name='room-report'),



]