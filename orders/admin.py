from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'pharmacy', 'medication', 'status', 'created_at']
    list_filter = ['status', 'pharmacy']
    list_editable = ['status']