from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Medication, PharmacyMedication
from .serializers import MedicationSerializer, PharmacyMedicationSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Medication.objects.all()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class PharmacyMedicationViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacyMedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = PharmacyMedication.objects.select_related('medication', 'pharmacy').all()

        q = self.request.query_params.get('q')
        pharmacy = self.request.query_params.get('pharmacy')
        in_stock = self.request.query_params.get('in_stock')

        if q:
            qs = qs.filter(medication__name__icontains=q)
        if pharmacy:
            qs = qs.filter(pharmacy__name__icontains=pharmacy)
        if in_stock == 'true':
            qs = qs.filter(stock__gt=0)

        return qs

    def perform_create(self, serializer):
        # Only verified pharmacies can add inventory via API
        user = self.request.user
        if user.role == 'pharmacy':
            try:
                serializer.save(pharmacy=user.pharmacy_profile)
                return
            except Exception:
                pass
        serializer.save()