from django.urls import path
from .views import manage_order

urlpatterns = [
    path('orders/<int:order_id>/manage/', manage_order, name='manage_order'),
]