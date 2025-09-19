from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RestrictedZone(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(help_text="Radius in meters")

    def __str__(self):
        return self.name


class EmergencyReport(models.Model):
    user_name = models.CharField(max_length=100)
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} @ {self.timestamp}"


class Profile(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
        ("police", "Police"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    def __str__(self):
        return f"{self.user.username} - {self.role}"

ROLE_CHOICES = (
    ('tourist', 'Tourist'),
    ('police', 'Police'),
    ('admin', 'Admin'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tourist')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
