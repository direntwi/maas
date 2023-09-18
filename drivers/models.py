from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from users.models import User
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver

# Create your models here.

class DriverManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DRIVER)
    


class Driver(User):
    base_role = User.Role.DRIVER
    driver = DriverManager() #use something like Driver.drivers.all() to get only drivers
    class Meta:
        proxy = True

@receiver(post_save, sender=Driver)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DRIVER":
        DriverProfile.objects.create(user=instance)


class VehicleManager(BaseUserManager):
    pass

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20) #consider a choices field
    make = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    seats = models.IntegerField()
    available_seats = models.IntegerField()

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_id = models.IntegerField(null=True, blank=True)
    vehicle = models.ManyToManyField(Vehicle)



