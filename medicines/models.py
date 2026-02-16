from django.db import models
from core.models import TimeStampedModel
from pharmacies.models import Pharmacy

class Medicine(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="medicines"
    )

    def __str__(self):
        return f"{self.name} - {self.pharmacy.name}"
