from django.db import models
from accounts.models import User
from pharmacies.models import Pharmacy


class Prescription(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prescriptions"
    )

    image = models.ImageField(upload_to='prescriptions/')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.id} - {self.status}"