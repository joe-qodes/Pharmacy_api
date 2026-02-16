from django.db import models
from core.models import TimeStampedModel

class Pharmacy(TimeStampedModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

