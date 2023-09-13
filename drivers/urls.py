from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router =DefaultRouter()
router.register('all-drivers', views.DriverViewSet)
router.register('vehicles', views.VehicleViewSet)
# router.register('login', views.LoginViewSet, basename='login')

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls,))
    #path function accepts 3 variables
    #route, the function in the views file and a name(not compulsory but good practice)
]