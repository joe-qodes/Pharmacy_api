from django.db import models
from accounts.models import User
from pharmacies.models import Pharmacy
from medications.models import Medication, PharmacyMedication
from prescriptions.models import Prescription

class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    pharmacy_medication = models.ForeignKey(
        PharmacyMedication,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} — {self.patient.username} → {self.medication.name} ({self.status})"