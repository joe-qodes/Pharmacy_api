from rest_framework import viewsets, permissions
from .models import Pharmacy
from .serializers import PharmacySerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)