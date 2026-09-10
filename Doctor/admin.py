from django.contrib import admin
from .models import Doctor, Patient, Booking

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Booking)