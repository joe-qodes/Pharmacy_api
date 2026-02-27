from django.db import models
from accounts.models import User
from pharmacies.models import Pharmacy
from prescriptions.models import Prescription


class Request(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests"
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="requests"
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="requests"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} - {self.status}"