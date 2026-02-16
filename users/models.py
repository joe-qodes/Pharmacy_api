from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('pharmacist', 'Pharmacist'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.role})"
