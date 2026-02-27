from rest_framework import serializers
from .models import Medication, PharmacyMedication


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class PharmacyMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyMedication
        fields = '__all__'