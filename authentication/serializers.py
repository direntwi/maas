from django.contrib.auth import authenticate

from users.models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

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

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb = urlsafe_base64_decode(user.id)
                
        except:
            pass

        return super().validate(attrs)


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