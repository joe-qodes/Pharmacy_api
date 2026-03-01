from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
     # patient details (visible to pharmacy)
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    patient_email = serializers.EmailField(source='patient.email', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone_number', read_only=True)

    # medication and pharmacy details
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    pharmacy_address = serializers.CharField(source='pharmacy.address', read_only=True)
    pharmacy_email = serializers.EmailField(source='pharmacy.user.email', read_only=True)
    pharmacy_phone = serializers.CharField(source='pharmacy.user.phone_number', read_only=True)

     # prescription
    prescription_image = serializers.ImageField(source='prescription.image', read_only=True)


    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['patient', 'status']