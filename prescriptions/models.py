from django.db import models
from core.models import TimeStampedModel
from users.models import User
from medicines.models import Medicine

class Prescription(TimeStampedModel):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    doctor_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField()

    def __str__(self):
        return f"Prescription #{self.id} - {self.patient.username}"
