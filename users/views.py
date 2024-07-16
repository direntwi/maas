from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Vehicle
from .serializers import UserSerializer, VehicleSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.all()
        return user
    

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(name=data['name'], phone_number=data['phone_number'], email=data['email'], password=data['password'], role=data['role'])
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        vehicle = Vehicle.objects.all()
        return vehicle
    
    def create(self, request, *args, **kwargs):
        # data= request.data
        # user_id= request.user.id
        # vehicle = Vehicle.objects.create(
        #                 registration_number=data['registration_number'],
        #                 make = data['make'],
        #                 colour=data['colour'],
        #                 seats = data['seats'],
        #                 available_seats = data['available_seats']
        #                 )
        # vehicle.save()
        # user = User.objects.get(id=user_id)
        # user.vehicles.add(vehicle)
        return Response({"request":request.user})
    

class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.all().filter(role=User.Role.DRIVER)
        return user
    
    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(name=data['name'], phone_number=data['phone_number'], email=data['email'], password=request.data.get('password'), role=User.Role.DRIVER)
        user.role="DRIVER"
        user.save()

        # if data['vehicles'] is not None:
        #     for vehicle in data['vehicles']:
        #         vehicle_obj = Vehicle.objects.get(registration_number=vehicle['registration_number'])
        #         if vehicle_obj is None:
        #             vehicle_obj = Vehicle.objects.create(
        #                 registration_number=vehicle['registration_number'],
        #                 make = vehicle['make'],
        #                 colour=vehicle['number'],
        #                 seats = vehicle['seats'],
        #                 available_seats = vehicle['available_seats']
        #                 )
        #         user.vehicles.add(vehicle_obj)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        



class LoginViewSet(viewsets.ViewSet):
    """checks phone number and password"""
    serializer_class = AuthTokenSerializer
    

    def create(self, request):
        return ObtainAuthToken().as_view()(request=request._request)
    

