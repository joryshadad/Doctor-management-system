from django.contrib import admin

from .models import Booking, Doctor, DoctorProfile, Notification, Patient, Service


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone', 'is_active')
    list_filter = ('is_active', 'specialty', 'services')
    search_fields = ('name', 'specialty', 'phone')
    filter_horizontal = ('services',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'room_number')
    search_fields = ('doctor__name', 'room_number')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'phone')
    search_fields = ('name', 'phone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price')
    search_fields = ('service_name', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'doctor',
        'patient',
        'service',
        'price',
        'date',
        'time',
    )
    list_filter = ('date', 'service')
    search_fields = ('doctor', 'patient', 'service')
    ordering = ('-date', '-time')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
