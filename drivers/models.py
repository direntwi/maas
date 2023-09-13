from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.


class Driver(models.Model):
    name = models.CharField(max_length= 50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=50) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    is_active = models.BooleanField(default = False) #possibly to determine whether a driver is taking commuters

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
        return self.password == password




class Vehicle(models.Model):
    registration_number = models.CharField(primary_key=True, max_length=15)
    brand = models.CharField(max_length=20) #consider a choices field
    make = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    driver = models.ManyToManyField(Driver)
    seats = models.IntegerField()
    available_seats = models.IntegerField()

class Recover(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    password_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


