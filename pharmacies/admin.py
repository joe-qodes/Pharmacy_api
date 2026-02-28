from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'license_number', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    list_editable = ['is_verified']
    search_fields = ['name', 'license_number', 'user__username']