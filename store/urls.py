from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='root'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/read/', views.notification_read, name='notification_read'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/add/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('doctors/<int:pk>/profile/', views.doctor_profile_update, name='doctor_profile_update'),
    path('patients/', views.patients, name='patients'),
    path('booking/', views.booking, name='booking'),
]
