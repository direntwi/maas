from django.shortcuts import render


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


from .models import Driver, Vehicle
from . import serializers
from . import permissions
from . import models
# Create your views here.

class DriverViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating objects"""
    serializer_class = serializers.DriverSerializer
    queryset = Driver.driver.filter()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateDriverProfile,)




class LoginViewSet(viewsets.ViewSet):
    """checks phone number and password"""
    serializer_class = AuthTokenSerializer
    

    def create(self, request):
        return ObtainAuthToken().as_view()(request=request._request)
        


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()  # Define the queryset
    serializer_class = serializers.VehicleSerializer



# @api_view(['POST'])
# def add_vehicle(request):
#     current_user = request.user
#     serializer = serializers.VehicleSerializer()
#     if serializer.is_valid():
#         serializer.save()
#     # driver = Driver.driver.get(id=request.data['driver_id'])
#     # if driver is not None:
#     return Response({'data': request.data})

# class LinkDriverAndVehicleViewSet(viewsets.ViewSet):
#     queryset = models.DriverProfile.objects.filter(vehicle_name=)
    