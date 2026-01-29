# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import FamilyProfile, ProfessionalProfile, ServiceType

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "role", "is_staff", "is_active")
    search_fields = ("email",)
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("id",)

@admin.register(FamilyProfile)
class FamilyProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "display_name", "city", "zipcode", "user")
    search_fields = ("display_name", "user__email")
    ordering = ("id",)

@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "display_name", "city", "state", "zipcode", "user")
    search_fields = ("display_name", "user__email", "city", "state")
    ordering = ("id",)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    ordering = ("id",)
