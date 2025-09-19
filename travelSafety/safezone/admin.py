
from django.contrib import admin
from .models import RestrictedZone, EmergencyReport

admin.site.register(RestrictedZone)
admin.site.register(EmergencyReport)
