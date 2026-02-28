from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        if user.role == 'pharmacy':
            try:
                return Order.objects.filter(pharmacy=user.pharmacy_profile)
            except Exception:
                return Order.objects.none()
        return Order.objects.filter(patient=user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        order = self.get_object()
        self._check_pharmacy_owns(request, order)
        order.status = 'accepted'
        order.save()
        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        self._check_pharmacy_owns(request, order)
        order.status = 'rejected'
        order.save()
        return Response({'status': 'rejected'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        self._check_pharmacy_owns(request, order)
        order.status = 'completed'
        order.save()
        return Response({'status': 'completed'})

    def _check_pharmacy_owns(self, request, order):
        if request.user.role != 'pharmacy':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only pharmacies can update order status.")
        try:
            if order.pharmacy != request.user.pharmacy_profile:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("This order does not belong to your pharmacy.")
        except Exception:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("No pharmacy profile found.")


# HTML view for pharmacy to manage orders
def manage_order(request, order_id):
    if not request.user.is_authenticated or request.user.role != 'pharmacy':
        return redirect('login')

    try:
        pharmacy = request.user.pharmacy_profile
    except Exception:
        return redirect('dashboard')

    order = get_object_or_404(Order, id=order_id, pharmacy=pharmacy)
    new_status = request.POST.get('status')

    if new_status in ('accepted', 'rejected', 'completed'):
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.id} marked as {new_status}.')

    return redirect('dashboard')