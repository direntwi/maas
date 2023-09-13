from django.db import models
from commuters.models import Commuter
from drivers.models import Vehicle

# Create your models here.


class Booking(models.Model):
    commuter = models.ForeignKey(Commuter, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
