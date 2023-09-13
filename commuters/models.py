from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Commuter(AbstractUser):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=50)   
    email = models.EmailField(unique=True, null=True)

    #consider also:
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)

    def __str__(self):
        return self.name
    

    
    


