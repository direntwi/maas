from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    VehicleViewSet, UserViewSet, DriverViewSet, LoginViewSet,
    )


router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('vehicle', VehicleViewSet, basename='vehicle')
router.register('driver', DriverViewSet, basename='driver')
# router.register('login', LoginViewSet, basename='login')

urlpatterns = [
    
    path('', include(router.urls)),
]