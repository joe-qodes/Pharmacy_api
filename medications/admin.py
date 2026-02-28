from django.contrib import admin
from .models import Medication, PharmacyMedication


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category']


@admin.register(PharmacyMedication)
class PharmacyMedicationAdmin(admin.ModelAdmin):
    list_display = ['medication', 'pharmacy', 'stock', 'price']
    list_filter = ['pharmacy']