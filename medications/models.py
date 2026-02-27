from django.db import models
from pharmacies.models import Pharmacy


class Medication(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PharmacyMedication(models.Model):

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE
    )

    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medication.name} - {self.pharmacy.name}"