from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Vehicle
from .serializers import UserSerializer, VehicleSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
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
    

@api_view(['POST'])
def login_view(request):
    if request.method =='POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token_data = serializer.get_jwt_token(serializer.validated_data)
            return Response({
                "token_data" : token_data,
            }, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            response_data = {
                "message":"Login Failed",
                "errors": errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
              
            return Response({'success': True, 'message': 'Credentials are valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)


              
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
