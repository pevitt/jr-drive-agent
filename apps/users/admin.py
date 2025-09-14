from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'company', 'is_active']
    list_filter = ['is_active', 'is_staff', 'company', 'date_joined']
    search_fields = ['username', 'email', 'phone_number']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('phone_number', 'company')
        }),
    )
