from rest_framework import viewsets, permissions
from .models import Prescription
from .serializers import PrescriptionSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Prescription.objects.all()

        return Prescription.objects.filter(patient=user)