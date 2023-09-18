from rest_framework import serializers

from . import models


class DriverSerializer(serializers.Serializer):
    """A serializer for our driver objects"""

    class Meta:
        model = models.Driver
        fields = ('id', 'email', 'name', 'password', 'phone_number', 'latitude', 'longitude', 'is_active', 'role')
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        """Create and return a new user"""

        driver = models.Driver(
            email = validated_data['email'],
            name = validated_data['name'],
            phone_number = validated_data['phone_number']

        )

        driver.set_password(validated_data['password'])
        driver.save()
        return driver




class VehicleSerializer(serializers.ModelSerializer):
    """To find a list of all vehicles in a driver's profile"""


    class Meta:
        model = models.Vehicle
        fields = '__all__'


    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)








# class LinkDriverAndVehicleSerializer(serializers.Serializer):
#         driver_id = serializers.IntegerField()
#         vehicle_id = serializers.IntegerField()

#         def create(self, validated_data):
#             driver = models.DriverProfile.objects.get(id=validated_data['driver_id'])
#             vehicle = models.Vehicle.objects.get(id=validated_data['vehicle_id'])

#             driver.vehicle.add(vehicle)

#             return driver 