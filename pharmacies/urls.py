from django.urls import path
from .views import update_stock, add_medication

urlpatterns = [
    path('inventory/<int:pm_id>/update/', update_stock, name='update_stock'),
    path('inventory/add/', add_medication, name='add_medication'),
]