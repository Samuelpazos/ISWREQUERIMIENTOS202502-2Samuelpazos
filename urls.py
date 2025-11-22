from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('owner/new/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('pet/new/', views.PetCreateView.as_view(), name='pet_create'),
    path('appointment/new/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('medical-history/new/', views.MedicalHistoryCreateView.as_view(), name='medical_history_create'),
]
