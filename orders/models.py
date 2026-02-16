from django.db import models
from core.models import TimeStampedModel
from users.models import User
from pharmacies.models import Pharmacy
from prescriptions.models import Prescription

class Order(TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
