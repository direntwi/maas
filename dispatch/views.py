from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .models import Dispatch
from .serializers import DispatchSerializer

# Create your views here.

class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == User.Role.DRIVER:
    #         return self.queryset.filter(driver=user)
    #     elif user.role == User.Role.COMMUTER:
    #         return self.queryset.filter(commuter=user)
    #     return self.queryset
