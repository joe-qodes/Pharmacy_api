from rest_framework import viewsets, permissions
from .models import Medication, PharmacyMedication
from .serializers import MedicationSerializer, PharmacyMedicationSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PharmacyMedicationViewSet(viewsets.ModelViewSet):
    queryset = PharmacyMedication.objects.all()
    serializer_class = PharmacyMedicationSerializer
    permission_classes = [permissions.IsAuthenticated]