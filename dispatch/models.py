from django.db import models
from users.models import User, Vehicle
# Create your models here.


class Dispatch(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ACCEPTED', 'Accepted'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    driver = models.ForeignKey(User, related_name='driver_dispatches', on_delete=models.CASCADE)
    commuter = models.ForeignKey(User, related_name='commuter_dispatches', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='REQUESTED')
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.driver.name} -> {self.commuter.name} [{self.status}]"
