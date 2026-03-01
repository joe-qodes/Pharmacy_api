from rest_framework import serializers
from .models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Pharmacy
        fields = ['id', 'name', 'license_number', 'address', 'is_verified', 'created_at', 'email', 'phone_number']
        read_only_fields = ['user', 'is_verified']
