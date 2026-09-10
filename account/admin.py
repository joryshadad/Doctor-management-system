from django.contrib import admin
from .models import SystemUser

class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')

admin.site.register(SystemUser, SystemUserAdmin)