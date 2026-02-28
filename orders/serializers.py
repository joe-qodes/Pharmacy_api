from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['patient', 'status']