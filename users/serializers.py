from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Vehicle
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'name', 'email', 'phone_number','password', 'longitude', 'latitude', 'role', 'vehicles', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
        # fields = '__all__'
        depth = 1 


class LoginSerializer(serializers.Serializer):
    eop = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

    def validate(self, data):
        if not User.objects.filter(phone_number=data['eop']).exists() and not User.objects.filter(email=data['eop']).exists():
            raise serializers.ValidationError('User Does Not Exist')
        
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username= data['eop'],password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        
        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message':'Login Successful'
        }

        user_data= {
            'user_id' : user.id,
            'name': user.name,
            'role':user.role,
            'longitude' : user.longitude,
            'latitude' : user.latitude,
            'phone_number': user.phone_number,

        }
        token_data['user'] = user_data
        
        return token_data
        


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length= 50, min_length =2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=2, write_only = True)
    token = serializers.CharField(min_length=1, write_only = True)
    uidb64 = serializers.CharField(min_length=1, write_only = True)

    class Meta:
        fields = ['password', 'token', 'b64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
        
            user.set_password(password)
            user.save() 

            return (user)
        
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

