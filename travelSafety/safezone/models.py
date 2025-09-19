from django.db import models

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
