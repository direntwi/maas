from django.shortcuts import render, redirect
from .models import Driver, Vehicle, Recover
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import uuid
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets,filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from . import serializers, models, permissions

# Create your views here.

# def register_driver(aname, aphone_number, apassword, aemail=None):
#     new_driver = Driver(name=aname, phone_number=aphone_number, password=apassword, email=aemail)
#     #Driver(name='bofah',phone_number= '0265132547', email='bofah@gmail.com', password='nagi7w289') this format works
#     # if you don't follow this, the name ends up becoming the id
#     new_driver.save()
#     return new_driver.name, new_driver.phone_number


# def signup(request):
#     if request.method == "POST":
#         aname = request.POST['name']
#         aphone_number = request.POST['phone_number']
#         aemail = request.POST['email']
#         apassword = request.POST['password']
#         apassword2 = request.POST['password2']


#         if Driver.objects.filter(phone_number=aphone_number):
#             messages.error(request, "Phone number already exist! Please try some other username.")
#             return redirect()

#         if Driver.objects.filter(email=aemail).exists():
#             messages.error(request, "Email Already Registered!!")
#             return redirect()
        
#         if apassword != apassword2:
#             messages.error(request, "Passwords didn't match!!")
#             return redirect()
        
        
#         Driver.objects.create(name=aname, phone_number =aphone_number , email = aemail, password=apassword)
    


def signin(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]

        driver = authenticate(phone_number=phone_number, password=password)
        if driver is not None:
            login(request, driver)
        else:
            messages.error(request, "Incorrect login credentials")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect()


def change_password(request, token):
    #need to create a field for tokens to be added to driver fields in case they forget passwords
   
    recovery_object = Recover.objects.filter(password_token = token).first()
    context = {'driver_id': recovery_object.driver.name}

    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        driver_id = request.POST['driver_id']

        if new_password !=confirm_password:
            messages.error(request, 'Passwords do not match')

        driver = Driver.objects.get(id = driver_id)
        driver.set_password(new_password)
        # driver.password = new_password   use this if the line above does not work
        driver.save() 
        return redirect()



    



def send_recovery_email(email, token):
    subject = 'Reset Your Password'
    message = f'Click on the link to reset your password: http:/127.0.0.1:8000/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)
    return True



def password_recovery(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']


        driver = Driver.objects.get(phone_number = phone_number)
        token = str(uuid.uuid4())
        recovery_object = Recover.objects.get(driver = driver)
        recovery_object.password_token = token
        recovery_object.save()
        send_recovery_email(driver.email , token)
        messages.success(request, 'An email has been sent to your inbox')



     




#Vehicles
#add vehicles
def add_vehicle(request):
    if request.method =='POST':
        registration_number = request.POST['registraion_number']
        brand = request.POST['brand']
        make =request.POST['make']
        colour = request.POST['colour']
        seats = request.POST['seats']
        driver_id = request.POST['driver_id']
        

        # d = Driver.objects.get(id = driver_id)
        v=Vehicle.objects.create(registration_number=registration_number, brand =brand, make=make, colour=colour, seats=seats, available_seats = seats)
        v.driver.add(driver_id)

#edit vehicles
def edit_vehicle_data(request):
    if request.method == "POST":
        registration_number = request.POST['registraion_number']
        brand = request.POST['brand']
        make =request.POST['make']
        colour = request.POST['colour']
        seats = request.POST['seats']

        
        Vehicle.objects.filter(registration_number=registration_number).update(registration_number=registration_number, make=make, brand=brand, colour = colour, seats=seats)
     
    



#see all vehicles under a driver
def drivers_vehicles(request):
    if request.method == "POST":
        driver_id = request.POST['driver_id']

        d = Driver.objects.get(id=driver_id)

        v=Vehicle.objects.filter(driver = d)
    return v



def drivers_vehicle():
    driver_id = 158
    data = {}

    d = Driver.objects.get(id=driver_id)
    if d:
        data['driver name'] = d.name

    return data

# drivers_vehicle()








class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer


    def get(self, request, format = None):
        an_apiview =[
            'Uses HTTP methods as a function (get, post, patch, put, delete)',
            'It is similar to a traditional django view',
            'Gives you the most control over your logic',
            'It is mapped anually to URLs'
        ]

        return Response({'message':'Hello!', 'an_apiview':an_apiview})
    
    def post(self, request):
        """Create a hello message with our name"""

        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class DriverViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating drivers data"""


    serializer_class = serializers.DriverSerializer
    queryset = models.Driver.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateDriverProfile, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)





class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()  # Define the queryset
    serializer_class = serializers.VehicleSerializer


@api_view(['POST'])
def login(request):
    driver = get_object_or_404(Driver, name=request.data['name'])
    if not driver.check_password(request.data['password']):
        return Response({"detail":"Not found"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(driver=driver)
    serializer = serializers.DriverSerializer(instance=driver)
    return Response({"token": token.key, "user":serializer.data})


@api_view(['POST'])
def signup(request):
    
    serializer = serializers.DriverSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        driver = Driver.objects.get(name=request.data['name'])
        driver.save(request.data['password'])
        driver.save()
        token = Token.objects.create(driver=driver)
        return Response({"token": token.key, "user":serializer.data})
    return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


