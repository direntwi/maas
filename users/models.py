from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, phone_number, password, **other_fields):
        if not phone_number:
            raise ValueError('You must provide a phone number')
        user = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, name, email, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff = True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser = True')
        return self.create_user(name, email, phone_number, password, **other_fields)



class Vehicle(models.Model):
    registration_number = models.CharField(max_length=15)
    make = models.CharField(max_length=20) #consider a choices field
    model = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return self.registration_number





class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True, blank=True)
    vehicles = models.ManyToManyField(Vehicle)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS =['name', 'email']


    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        COMMUTER = "COMMUTER", "Commuter"
        DRIVER = "DRIVER", 'Driver'

    base_role= Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

