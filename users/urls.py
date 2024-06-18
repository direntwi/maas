from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    VehicleViewSet, UserViewSet, DriverViewSet, LoginViewSet, login_view,
    PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView
    )


router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('vehicle', VehicleViewSet, basename='vehicle')
router.register('driver', DriverViewSet, basename='driver')
# router.register('login', LoginViewSet, basename='login')

urlpatterns = [
    
    path('', include(router.urls)),
    # path('login', login_view),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete')

]