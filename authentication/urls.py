from django.urls import path, include
from .views import (
        login_view, RequestPasswordResetEmail, SetNewPasswordAPIView, 
        PasswordTokenCheckAPI
        )



urlpatterns = [
        path('login', login_view),
        path('request-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
        path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
        path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete')

]