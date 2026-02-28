from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            role='patient',
        )


class PharmacyRegisterSerializer(serializers.Serializer):
    # Account fields
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(required=False, default='')

    # Pharmacy profile fields
    pharmacy_name = serializers.CharField()
    license_number = serializers.CharField()
    address = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        from pharmacies.models import Pharmacy

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            role='pharmacy',
        )

        Pharmacy.objects.create(
            user=user,
            name=validated_data['pharmacy_name'],
            license_number=validated_data['license_number'],
            address=validated_data['address'],
            is_verified=False,
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']