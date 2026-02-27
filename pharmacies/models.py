from django.db import models
from accounts.models import User


class Pharmacy(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pharmacy_profile"
    )

    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name