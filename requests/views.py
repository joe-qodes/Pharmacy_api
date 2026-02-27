from rest_framework import viewsets, permissions
from .models import Request
from .serializers import RequestSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Request.objects.all()

        return Request.objects.filter(patient=user)