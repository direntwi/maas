from rest_framework import serializers

from . import models

class HelloSerializer(serializers.Serializer):
    """A name field for testing our APIView."""
    name = serializers.CharField(max_length = 10)



class DriverSerializer(serializers.ModelSerializer):
    """A serializer for our driver objects"""

    class Meta:
        model = models.Driver
        fields = ('id', 'email', 'name', 'password', 'phone_number', 'latitude', 'longitude', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        """Create and return a new user"""

        driver = models.Driver(
            email = validated_data['email'],
            name = validated_data['name'],
            phone_number = validated_data['phone_number']

        )

        driver.save(validated_data['password'])
        driver.save()
        return driver









class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehicle
        fields = ('registration_number', 'brand', 'make', 'colour', 'seats', 'available_seats')

        
    def create(self, validated_data):
        """Create and return a new user"""

        vehicle = models.Vehicle(
            registration_number = validated_data['registration_number'],
            brand = validated_data['brand'],
            make = validated_data['make'],
            colour = validated_data['colour'],
            seats = validated_data['seats'],
            available_seats = validated_data['seats']

        )

        vehicle.save()
        return vehicle
    