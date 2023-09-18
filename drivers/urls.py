from django.urls import path, include  

from rest_framework.routers import DefaultRouter

from .  import views

router = DefaultRouter()
router.register('profile', views.DriverViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('vehicles', views.VehicleViewSet)



urlpatterns =[
    path('', include(router.urls,)),

]