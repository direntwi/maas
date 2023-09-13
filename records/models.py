from django.db import models
from commuters.models import Commuter
from drivers.models import Vehicle

# Create your models here.


class Records(models.Model):
    commuter = models.ForeignKey(Commuter, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(primary_key=True, auto_now=True)#be clear on what time it's supposed to record and set constraint accordingly
    status = models.CharField(max_length=20)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)